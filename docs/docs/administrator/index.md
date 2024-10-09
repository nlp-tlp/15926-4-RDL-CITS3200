# Administrator

This section contains information about how to update and view the data being served through the server in deployment through the CLI.

Once the CLI has been run, it will automatically provide brief explanations of what the choices you can make are.

## Accessing the CLI

### Lightsail in-browser SSH

Log into AWS, and select the Lightsail service to go to the Lightsail webapp. Select the instance for the iso15926vis deployment, and click on "Connect using SSH". You should be redirected to a browser-based terminal, which is the production environment.

To access the production CLI run either the command `cli` or

```bash
docker exec -it Server /app/cli.py
```

The first command has been set as an alias for the full docker command.

### Local SSH

To SSH from a local terminal instead of through AWS each time, download the instance's SSH keys from the Lightsail webapp described above. It will be named something like `LightsailDefaultKey.pem`. Set the permissions on the downloaded keys to be executable.

To SSH into the instance anytime after, run in a local terminal, replacing `<public-ip>` with the public IP address of the instance:

```bash
ssh -i LightsailDefaultKey.pem ubuntu@<public-ip>
```

Again, to access the production CLI run either the command `cli` or

```bash
docker exec -it Server /app/cli.py
```

## CLI functionality

When run, the CLI specifies what choices you can make on each menu.

The main CLI menu has:
**Q** = Quit the program\
**V** = Check the version, which shows you the current RDL .ttl file that is in use as well as when it was created\
**U** = Update the database, which will create a new .ttl file from the data on [https://data.15926.org/rdl](https://data.\15926.org/rdl) and reload the server's graph if it is running.\
**M** = Modify the database in use.

If you choose option **M**, you will be directed to another menu with choices:\
**D** = Delete a database, which will let you choose a .ttl file to delete\
**C** = Change the current database in use, which will show you all the .ttl files you have stored and which you can switch between.\
**Q** = Return to the previous menu.\
