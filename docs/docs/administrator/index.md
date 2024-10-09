# Administrator

This section contains information about how to update and view the data being served through the server in deployment through the CLI.

Once the CLI has been run, it will automatically provide brief explanations of what the choices you can make are.

## Accessing the CLI

### Access on local deployment

If the project is being hosted locally through docker, make sure the server container is running. The CLI can simply be accessed through the command

```bash
docker exec -it Server /app/cli.py
```

### Access on production deployment

The command to change or view the data on the production environment is the same, but you will need access to the production environment. This can either be done through the AWS Lightsail in-browser SSH feature, or by using SSH directly to the Lightsail instance.

#### Accessing Lightsail SSH

Log into AWS, and select the Lightsail service to go to the Lightsail webapp. Select the instance for the iso15926vis deployment, and click on "Connect using SSH". You should be redirected to a browser-based terminal, which is the production environment.

Then, run the same docker command to access the CLI.

```bash
docker exec -it Server /app/cli.py
```
