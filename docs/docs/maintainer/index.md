# Maintainer

This section contains information about how to reach the production environment as well as some useful commands.

## Accessing the production environment

#### Accessing Lightsail SSH

Log into AWS, and select the Lightsail service to go to the Lightsail webapp. Select the instance for the iso15926vis deployment, and click on "Connect using SSH". You should be redirected to a browser-based terminal, which is the production environment.

Then, run the same docker command to access the CLI.

```bash
docker exec -it Server /app/cli.py
```
