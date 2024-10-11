# IPMI and NVIDIA GPU Temperature Monitor with Fan Control

This application monitors IPMI sensors and NVIDIA GPUs, manages dynamic fan control, and presents a secure, mobile-friendly web interface for temperature monitoring and fan control.

## Quick Start

Use the following Docker run command to pull, build, and run the container:

docker run -d --name ipmi-gpu-monitor -p 8443:8443 -e SECRET_KEY=mysecretkey -e DEFAULT_USERNAME=admin -e DEFAULT_PASSWORD=admin -e IPMI_ADDRESS=your_ipmi_address -e IPMI_USERNAME=your_ipmi_username -e IPMI_PASSWORD=your_ipmi_password -v temperature_logs:/app/temperature_logs --restart unless-stopped docker.io/hrtsv/ipmi-nvidia-gpu-fanmanager:latest

Replace the following values with your actual configuration:
- mysecretkey: A secure secret key for the application
- your_ipmi_address: The IP address or hostname of your IPMI-enabled server
- your_ipmi_username: The username for IPMI access
- your_ipmi_password: The password for IPMI access

If you have NVIDIA GPUs and want to monitor them, add the following device mappings to the Docker run command:

--device /dev/nvidia0:/dev/nvidia0 --device /dev/nvidiactl:/dev/nvidiactl

Access the web interface at https://your_server_ip:8443

Default login credentials:
- Username: admin
- Password: admin

**Important:** Change the default password immediately after your first login.

## Troubleshooting

Check the Docker logs for any error messages or warnings:

docker logs ipmi-gpu-monitor

## License

This project is licensed under the MIT License - see the LICENSE file for details.
