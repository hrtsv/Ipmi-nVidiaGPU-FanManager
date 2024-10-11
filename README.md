# Temperature Monitor and Fan Control

This application monitors system temperatures and controls fan speeds using IPMI and NVIDIA Management Library.

## Prerequisites

- Docker
- NVIDIA GPU (optional for GPU temperature monitoring)

## Running the Application

To run the application using Docker, use the following command:

```bash
docker run --name tempmonitorfancontrol --privileged --network host \
-v ${PWD}/app:/app \
-v /sys:/sys:ro \
-e PYTHONUNBUFFERED=1 \
-e DEFAULT_USERNAME=admin \
-e DEFAULT_PASSWORD=admin \
-e IPMI_ADDRESS=localhost \
-e IPMI_USERNAME=ipmi_user \
-e IPMI_PASSWORD=ipmi_password \
-e DEBIAN_FRONTEND=noninteractive \
--gpus all \
--restart unless-stopped \
ubuntu:22.04 \
bash -c 'apt-get update && \
apt-get install -y python3 python3-pip python3-venv openssl ipmitool curl && \
python3 -m venv /app/venv && \
. /app/venv/bin/activate && \
pip install flask flask-restx pyjwt nvidia-ml-py3 tenacity && \
python3 /app/app.py'
```

This command will start the application in a Docker container with the necessary configurations.

Note: Make sure that the `app` directory containing `app.py` is in the current working directory when running this command.

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
