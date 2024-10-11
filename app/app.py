import os
import time
import subprocess
import re
import logging
from flask import Flask, request, send_from_directory, jsonify
from flask_restx import Api, Resource, fields, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import sqlite3
from datetime import datetime, timedelta
import pynvml
from tenacity import retry, stop_after_attempt, wait_fixed
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='', static_folder='.')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
api = Api(app, version='1.0', title='Temperature Monitor API', description='A simple Temperature Monitor API', doc='/api')

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Constants and Configuration
DB_FILE = 'temperature_logs.db'
TEMP_THRESHOLDS = {
    'CPU': {'low': 50, 'high': 70},
    'RAM': {'low': 40, 'high': 60},
    'GPU0': {'low': 50, 'high': 75},
    'GPU1': {'low': 50, 'high': 75},
    'CASE': {'low': 35, 'high': 45}
}
FAN_MIN, FAN_MAX = 10, 100

# Load configuration from environment variables
DEFAULT_USERNAME = os.environ.get('DEFAULT_USERNAME', 'admin')
DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD', 'admin')
IPMI_ADDRESS = os.environ.get('IPMI_ADDRESS', 'localhost')
IPMI_USERNAME = os.environ.get('IPMI_USERNAME', 'ipmi_user')
IPMI_PASSWORD = os.environ.get('IPMI_PASSWORD', 'ipmi_password')

# User configuration
USERS = {DEFAULT_USERNAME: generate_password_hash(DEFAULT_PASSWORD)}

# Database initialization
def init_db():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS temperature_logs
                            (timestamp INTEGER, cpu_temp REAL, ram_temp REAL, gpu0_temp REAL, gpu1_temp REAL, case_temp REAL)''')
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")

# Temperature monitoring
try:
    pynvml.nvmlInit()
except pynvml.NVMLError as e:
    logger.error(f"NVML initialization error: {e}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_gpu_temps():
    temps = {}
    try:
        device_count = pynvml.nvmlDeviceGetCount()
        for i in range(min(device_count, 2)):  # Limit to 2 GPUs
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            temps[f'GPU{i}'] = temp
    except pynvml.NVMLError as error:
        logger.error(f"Error getting GPU temperatures: {error}")
    return temps

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_ipmi_temps():
    try:
        cmd = ['ipmitool', '-H', IPMI_ADDRESS, '-U', IPMI_USERNAME, '-P', IPMI_PASSWORD, 'sdr', 'type', 'temperature']
        output = subprocess.check_output(cmd, universal_newlines=True, timeout=10)
        temps = {'CPU': None, 'RAM': None, 'CASE': None}
        for line in output.splitlines():
            if 'CPU' in line: temps['CPU'] = int(re.search(r'(\d+) degrees C', line).group(1))
            elif 'RAM' in line: temps['RAM'] = int(re.search(r'(\d+) degrees C', line).group(1))
            elif 'Ambient' in line or 'System Temp' in line: temps['CASE'] = int(re.search(r'(\d+) degrees C', line).group(1))
        return temps
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing IPMI command: {e}")
    except subprocess.TimeoutExpired:
        logger.error("IPMI command timed out")
    except Exception as e:
        logger.error(f"Unexpected error in get_ipmi_temps: {e}")
    return None

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def set_fan_speed(speed):
    try:
        cmd = ['ipmitool', '-H', IPMI_ADDRESS, '-U', IPMI_USERNAME, '-P', IPMI_PASSWORD, 'raw', '0x30', '0x30', '0x02', hex(speed)]
        subprocess.run(cmd, check=True, timeout=10)
        logger.info(f"Fan speed set to {speed}%")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting fan speed: {e}")
    except subprocess.TimeoutExpired:
        logger.error("Fan speed command timed out")
    except Exception as e:
        logger.error(f"Unexpected error in set_fan_speed: {e}")

def calculate_fan_speed(current_temp, low_threshold, high_threshold):
    if current_temp <= low_threshold: return FAN_MIN
    if current_temp >= high_threshold: return FAN_MAX
    temp_range = high_threshold - low_threshold
    temp_above_low = current_temp - low_threshold
    speed_range = FAN_MAX - FAN_MIN
    return FAN_MIN + (temp_above_low / temp_range) * speed_range

# JWT token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing!'}, 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired!'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token!'}, 401
        return f(*args, **kwargs)
    return decorated

# API models
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(user_model)
    @limiter.limit("5 per minute")  # Add rate limiting to login endpoint
    def post(self):
        auth = request.json
        if not auth or not auth['username'] or not auth['password']:
            return {'message': 'Could not verify'}, 401
        if auth['username'] in USERS and check_password_hash(USERS[auth['username']], auth['password']):
            token = jwt.encode({'username': auth['username'], 'exp': datetime.utcnow() + timedelta(hours=24)}, app.config['SECRET_KEY'])
            return {'token': token}
        return {'message': 'Could not verify'}, 401

@api.route('/temperatures')
class Temperatures(Resource):
    @token_required
    def get(self):
        gpu_temps = get_gpu_temps()
        ipmi_temps = get_ipmi_temps() or {}
        all_temps = {**gpu_temps, **ipmi_temps}
        
        max_fan_speed = FAN_MIN
        for component, temp in all_temps.items():
            if temp is not None and component in TEMP_THRESHOLDS:
                fan_speed = calculate_fan_speed(temp, TEMP_THRESHOLDS[component]['low'], TEMP_THRESHOLDS[component]['high'])
                max_fan_speed = max(max_fan_speed, fan_speed)
        
        set_fan_speed(int(max_fan_speed))
        
        try:
            with sqlite3.connect(DB_FILE) as conn:
                conn.execute("INSERT INTO temperature_logs VALUES (?, ?, ?, ?, ?, ?)",
                             (int(time.time()), ipmi_temps.get('CPU'), ipmi_temps.get('RAM'),
                              gpu_temps.get('GPU0'), gpu_temps.get('GPU1'), ipmi_temps.get('CASE')))
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
        
        return {'temperatures': all_temps, 'fan_speed': max_fan_speed}

parser = reqparse.RequestParser()
parser.add_argument('hours', type=int, required=True, help='Number of hours for historical data')

@api.route('/historical_data')
class HistoricalData(Resource):
    @token_required
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        hours = args['hours']
        start_time = int(time.time()) - hours * 3600
        try:
            with sqlite3.connect(DB_FILE) as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM temperature_logs WHERE timestamp > ? ORDER BY timestamp", (start_time,))
                data = c.fetchall()
            return {'data': data}
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return {'message': 'Error retrieving historical data'}, 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    try:
        # Check if we can connect to the database
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("SELECT 1")
        
        # Check if we can get GPU temperatures
        get_gpu_temps()
        
        # Check if we can get IPMI temperatures
        get_ipmi_temps()
        
        return jsonify(status="healthy"), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify(status="unhealthy", error=str(e)), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # Now you're handling non-HTTP exceptions only
    logger.error(f"An unexpected error occurred: {str(e)}")
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8443, ssl_context=('cert.pem', 'key.pem'))
