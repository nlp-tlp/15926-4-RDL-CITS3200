# Accessing and using Lightsail

This page describes how to access and deal with the server and client code in production.

## Accessing production environment

The production environment can be accessed through the AWS Lightsail in-browser SSH feature, or by using SSH directly to the Lightsail instance.

### Lightsail in-browser SSH

Log into AWS, and select the Lightsail service to go to the Lightsail webapp. Select the instance for the iso15926vis deployment. Here you can access metrics for the instance as well as any firewall rules.

From here you can also access the production system by clicking on "Connect using SSH". You should be redirected to a browser-based terminal, which is the production environment.

### Local SSH

To SSH from a local terminal instead of through AWS each time, download the instance's SSH keys from the Lightsail webapp described above. It will be named something like `LightsailDefaultKey.pem`. Set the permissions on the downloaded keys to be executable.

To SSH into the instance anytime after, run in a local terminal, replacing `<public-ip>` with the public IP address of the instance:

```bash
ssh -i LightsailDefaultKey.pem ubuntu@<public-ip>
```

## Stopping or reloading containers

### Stopping containers

To stop all the currently-running containers, run the docker command:

```bash
docker compose down
```

### Restarting containers

To bring up the server, client, and Traefik containers, run:

```bash
docker compose up
```

Add `-d` if you don't want to see the continued logging of the containers.

## Other instructions

### Checking Docker logs

To check Docker logs for errors, run:

```bash
docker-compose logs
```

### Removing errored images

If images fail to run, or are built over, they can be viewed through

```bash
docker images
```

and deleted with

```bash
docker image prune
```
