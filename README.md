# Temperature Monitor and Fan Control for IPMI and NVIDIA GPUs

This application monitors temperatures from IPMI sensors and NVIDIA GPUs, adjusts fan speeds based on temperature thresholds, and provides a web interface for viewing temperature data and historical logs.

## Features

- Real-time temperature monitoring for CPU, RAM, Case, and up to two NVIDIA GPUs
- Automatic fan speed adjustment based on configurable temperature thresholds
- Historical temperature data logging and retrieval
- Secure API with JWT authentication
- Health check endpoint for monitoring application status

## Deployment Instructions

1. In Dockge, create a new stack.
2. When prompted for the stack's source, choose "Git Repository".
3. Enter the URL of this GitHub repository.
4. Review and adjust the `compose.yaml` file if needed (see Configuration section).
5. Deploy the stack.

After deployment, access the Temperature Monitor at `https://your-server-ip:8443`.
Default login credentials are admin/admin. Change these immediately after first login.

## Configuration

Edit the `compose.yaml` file to adjust the following settings before deployment:

- `DEFAULT_USERNAME` and `DEFAULT_PASSWORD`: Change these to secure your application
- `IPMI_ADDRESS`, `IPMI_USERNAME`, and `IPMI_PASSWORD`: Set these to match your IPMI configuration
- Adjust the `TEMP_THRESHOLDS` in `app/app.py` if you need different temperature ranges for fan control

## Customization

The application is designed to be easily customizable:

- Modify `app/app.py` to add new features or adjust existing functionality
- Edit `app/index.html` to customize the web interface

After making changes, rebuild and redeploy the Docker container.

## Health Check

The application includes a health check endpoint at `/health`. This is used by Docker to monitor the application's status. You can also use this endpoint for external monitoring tools.

## Security Note

- Change the default credentials immediately after first login
- Ensure proper network security measures are in place to protect access to the application
- The application uses a self-signed SSL certificate by default. For production use, consider using a properly signed certificate

## Troubleshooting

- Check the Docker logs for any error messages
- Use the `/health` endpoint to verify if all components of the application are functioning correctly
- Ensure that the IPMI and NVIDIA GPU tools are properly installed and configured on the host system

## Contributing

Contributions to improve the application are welcome. Please submit pull requests or open issues on the GitHub repository.
