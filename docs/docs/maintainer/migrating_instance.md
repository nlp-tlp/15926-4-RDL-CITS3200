# Migrating instances

The current production website is hosted on AWS Lightsail. Here are instructions for if the instance needs to be shut down or a new instance needs to be set up the same way.

## Shutting down Lightsail instance

### Detaching static IP address

In the AWS Lightsail web app, select the iso15926vis instance. In the instance management go to the Networking tab, where you will see a pin icon under the public IPv4 address. Select it to go to the the details of the Static IP address.

If you want to stop hosting an instance altogether, make sure to the delete the instance. If not, simply detach the IP from the instance and reassign it to the new instance later.

### Deleting the Lightsail instance

Back in the management console for the instance, stop the instance and delete it.

### Removing Github autodeployment pipeline

If you do not intend to initialise another Lightsail instance, or use a similar service, disable or remove the Lightsail deploy pipeline from Github.

## Initialising Lightsail instance

### Create Lightsail instance

From the AWS Lightsail webapp, create a new instance and choose the packages and configurations you want. Choose a region for the instance to be in that is closest to where your users will be located.

The instance can run on a 1GB RAM instance but has best performance on a 2GB RAM instance. The following steps are based on Ubuntu.

### Assigning static IP address

A static IP address is required to ensure that the public IP address of the instance will not change after stopping and starting again.

In the Networking tab of the instance's management console, choose Create static IP, or just assign an IP address if you already have a static IP.

Note that static IP addresses can only be attached to instances in the same region.

### Lightsail Docker initialisation

To set up Docker on the instance, follow these commands in order (or use any equivalent docker installation steps).

First, install Docker:

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install docker and docker compose
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Enable Docker on the system with

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Add the user to a Docker group so that sudo doesn't have to be run each time with:

```bash
sudo usermod -aG docker ubuntu
newgrp docker
```

### Opening ports

In the Networking tab of the instance management console, make new rules to open up ports 80 (HTTP) and 443 (HTTPS), and any other ports you want open for the project to run.

### Github auto-deployment setup

To use the auto-deployment setup in the Github repo, you need to set up Github to use SSH. For more information about this pipeline, go to the Developer documentation's CI/CD section.

Go to the Lightsail instance management console, as mentioned before. Download the SSH key for the instance in the Connect tab. It will be named something similar to `LightsailDefaultKey.pem`. Also take note of the public IP address of the instance.

Go to Github secrets. In settings, select 'Secrets and variables', then 'Actions', then 'New repository secret'. For the secret `LIGHTSAIL_SSH_PRIVATE_KEY` copy and paste the full contents of the `.pem` file downloaded earlier. For `LIGHTSAIL_HOST`, enter the public IP address of the instance.
