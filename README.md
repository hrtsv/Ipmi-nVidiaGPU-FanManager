# Ipmi-nVidiaGPU-Temp-Monitor-Fan-Control
 Uses IPMI and nVidia gpu to monitor temeratures and adjust fan speeds
# Temperature Monitor for Dockge

This repository contains a Temperature Monitor application designed to be easily deployed using Dockge.

## Deployment Instructions

1. In Dockge, create a new stack.
2. When prompted for the stack's source, choose "Git Repository".
3. Enter the URL of this GitHub repository.
4. Deploy the stack.

After deployment, access the Temperature Monitor at `https://your-server-ip:8443`.
Default login credentials are admin/admin. Change these immediately after first login.

## Configuration

Edit the `compose.yaml` file to adjust environment variables such as IPMI settings before deployment.

## Security Note

Ensure to change the default credentials and properly secure access to the application.
