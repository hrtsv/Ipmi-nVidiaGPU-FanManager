# Temperature Monitor and Fan Control

This application monitors system temperatures and controls fan speeds using IPMI and NVIDIA Management Library.

## Prerequisites

- Docker
- NVIDIA GPU (optional for GPU temperature monitoring)

## Running the Application

To run the application using Docker, use the following command:

```bash
docker run --name temp-monitor-fan-control --privileged --network host \
-v "/app:/app" \
-v "/sys:/sys:ro" \
-e PYTHONUNBUFFERED=1 -e DEFAULT_USERNAME=admin -e DEFAULT_PASSWORD=admin \
-e IPMI_ADDRESS=localhost -e IPMI_USERNAME=ipmi_user -e IPMI_PASSWORD=ipmi_password \
-e DEBIAN_FRONTEND=noninteractive --gpus all \
--restart unless-stopped --health-cmd="curl -k https://localhost:8443/health" \
--health-interval=1m --health-timeout=10s --health-retries=3 --health-start-period=40s \
ubuntu:22.04 bash -c "
apt-get update &&
apt-get install -y --no-install-recommends python3 python3-pip openssl ipmitool software-properties-common curl &&
add-apt-repository ppa:graphics-drivers/ppa &&
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add - &&
curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu20.04/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list &&
apt-get update &&
apt-get install -y nvidia-container-toolkit-base &&
pip3 install flask flask-restx pyjwt nvidia-ml-py3 tenacity &&
if [ ! -f /app/cert.pem ] || [ ! -f /app/key.pem ]; then
  openssl req -x509 -newkey rsa:4096 -nodes -out /app/cert.pem -keyout /app/key.pem -days 365 -subj '/CN=localhost';
fi &&
python3 /app/app.py
"
```

This command will start the application in a Docker container with the necessary configurations.

## Features

- Monitors CPU, RAM, GPU, and case temperatures.
- Controls fan speeds based on temperature thresholds.
- Provides a RESTful API for accessing temperature data and controlling the application.

## API Endpoints

- `/login`: Authenticate and receive a JWT token.
- `/temperatures`: Get current temperature readings and fan speed.
- `/historical_data`: Retrieve historical temperature data.

## License

This project is licensed under the MIT License.
