# IPMI and NVIDIA GPU Temperature Monitor with Fan Control

This application monitors IPMI sensors and NVIDIA GPUs, manages dynamic fan control, and presents a secure, mobile-friendly web interface for temperature monitoring and fan control.

## Features

- Real-time monitoring of IPMI sensors and NVIDIA GPU temperatures
- Dynamic fan control based on temperature thresholds
- Secure web interface with JWT authentication and HTTPS
- Historical temperature data and charts
- Dockerized for easy deployment and configuration

## Prerequisites

- Docker
- IPMI-enabled server with NVIDIA GPUs

## Quick Start

Use the following Docker run command to fetch the latest version of the application, build it, and start it:

docker run -d \
  --name ipmi-gpu-monitor \
  -p 8443:8443 \
  -e SECRET_KEY=$(openssl rand -hex 32) \
  -e DEFAULT_USERNAME=admin \
  -e DEFAULT_PASSWORD=admin \
  -e IPMI_ADDRESS=your_ipmi_address \
  -e IPMI_USERNAME=your_ipmi_username \
  -e IPMI_PASSWORD=your_ipmi_password \
  --device /dev/nvidia0:/dev/nvidia0 \
  --device /dev/nvidiactl:/dev/nvidiactl \
  --device /dev/nvidia-modeset:/dev/nvidia-modeset \
  --device /dev/nvidia-uvm:/dev/nvidia-uvm \
  -v temperature_logs:/app/temperature_logs \
  --restart unless-stopped \
  $(docker build -q https://github.com/hrtsv/Ipmi-nVidiaGPU-FanManager.git)

Replace `your_ipmi_address`, `your_ipmi_username`, and `your_ipmi_password` with your actual IPMI configuration.

Access the web interface at `https://your_server_ip:8443`

Default login credentials:
- Username: admin
- Password: admin

**Important:** Change the default password immediately after your first login.

## Configuration

The application is pre-configured with the Docker run command. The only values you need to replace are:

- `IPMI_ADDRESS`: The IP address or hostname of your IPMI-enabled server
- `IPMI_USERNAME`: The username for IPMI access
- `IPMI_PASSWORD`: The password for IPMI access

All other configuration is handled automatically:
- `SECRET_KEY`: Automatically generated for securing the application
- `DEFAULT_USERNAME`: Set to "admin"
- `DEFAULT_PASSWORD`: Set to "admin"

## Security Considerations

- The application generates a self-signed SSL certificate during the Docker build process. For production use, consider replacing it with a certificate from a trusted Certificate Authority.
- Change the default password immediately after your first login.
- Use strong, unique passwords for user accounts and IPMI access.
- Limit access to the application to trusted networks only.

## Troubleshooting

- If you encounter issues with IPMI or GPU temperature readings, ensure that you have the necessary permissions and that the IPMI and NVIDIA drivers are properly installed on the host system.
- Check the Docker logs for any error messages or warnings:
  ```
  docker logs ipmi-gpu-monitor
  ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
