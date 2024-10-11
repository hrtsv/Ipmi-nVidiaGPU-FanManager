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

Use the following single command to pull the repository, build the Docker image, and run the container:

docker run -d --name ipmi-gpu-monitor -p 8443:8443 -e SECRET_KEY=mysecretkey -e DEFAULT_USERNAME=admin -e DEFAULT_PASSWORD=admin -e IPMI_ADDRESS=your_ipmi_address -e IPMI_USERNAME=your_ipmi_username -e IPMI_PASSWORD=your_ipmi_password --device /dev/nvidia0:/dev/nvidia0 --device /dev/nvidiactl:/dev/nvidiactl --device /dev/nvidia-modeset:/dev/nvidia-modeset --device /dev/nvidia-uvm:/dev/nvidia-uvm -v temperature_logs:/app/temperature_logs --restart unless-stopped docker build -t ipmi-gpu-monitor https://github.com/hrtsv/Ipmi-nVidiaGPU-FanManager.git#main && docker run -d --name ipmi-gpu-monitor ipmi-gpu-monitor

Replace the following values with your actual configuration:
- mysecretkey: A secure secret key for the application
- your_ipmi_address: The IP address or hostname of your IPMI-enabled server
- your_ipmi_username: The username for IPMI access
- your_ipmi_password: The password for IPMI access

Access the web interface at https://your_server_ip:8443

Default login credentials:
- Username: admin
- Password: admin

**Important:** Change the default password immediately after your first login.

## Configuration

The application is pre-configured with the Docker run command. The only values you need to replace are:

- SECRET_KEY: A secure secret key for the application
- IPMI_ADDRESS: The IP address or hostname of your IPMI-enabled server
- IPMI_USERNAME: The username for IPMI access
- IPMI_PASSWORD: The password for IPMI access

## Security Considerations

- Use a strong, unique SECRET_KEY for your application.
- Change the default password immediately after your first login.
- Use strong, unique passwords for user accounts and IPMI access.
- Limit access to the application to trusted networks only.
- The application uses HTTPS, but for production use, consider replacing the self-signed certificate with one from a trusted Certificate Authority.

## Troubleshooting

- If you encounter issues with IPMI or GPU temperature readings, ensure that you have the necessary permissions and that the IPMI and NVIDIA drivers are properly installed on the host system.
- Check the Docker logs for any error messages or warnings:

  docker logs ipmi-gpu-monitor

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
