<h1 align="center">
  <br>
  ISO15926vis
  <br>
</h1>
<h4 align="center">Web interface to visualise the ISO 15926 Reference Data Library.</h4>
<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#getting-started">Getting started</a> •
  <a href="#development">Development</a> •
  <a href="#deployment">Deployment</a> •
  <a href="#credits">Credits</a>
</p>

## Introduction

ISO15926vis is an interactive graph visualisation for the equipment Reference Data Library (RDL) described in the [ISO 15926-4 Standard](https://15926.org/).

This project assists in navigating the hierarchical relationships of classes defined by the RDL, accessible through the [current RDL browser](https://data.15926.org/rdl/) on which the hierarchy can be difficult to interpret.

🚧 This project is currently in the early stages of development and many things are subject to change. 🚧

## Getting started

These instructions will [install dependencies](#installing-dependencies) get a copy of the project [up and running](#running-the-project) on your local machine. This is also needed for testing and deployment.

### Installing dependencies

This project consists of a Vue client, Flask server, and command-line interface. Dependencies must first be installed before running any of these.

#### Git clone

Git clone the repository:

```
git clone https://github.com/nlp-tlp/15926-4-RDL-CITS3200.git
```

#### Setup script

A script is available to automatically run all the steps listed below for client and server dependencies.

⚠️ The script was built for Linux systems and your system may not be compatible. If you cannot follow these instructions on your OS, you can install dependencies manually following the sections below. ⚠️

The script requires Python Venv to run. If not already installed, run (on Linux):

```
sudo apt update
sudo apt install python3-venv
```

In the root directory, run:

```
./setup.sh
```

If you encounter the error `-bash: ./setup.sh: /bin/bash^M: bad interpreter: No such file or directory` and you are using WSL, run `sed -i 's/\r$//' setup.sh` then rerun the script.

#### Client dependency installation

If you intend to run the client, download [NVM](https://github.com/nvm-sh/nvm) from the official source or using a package manager for your OS.

Then, use NVM to install [NPM](https://nodejs.org/en/download/package-manager):

```
nvm install 20
nvm use 20
```

Install NPM dependencies in the main directory for [Husky Git hooks](https://typicode.github.io/husky/) and initialise Husky:

```
npm i
npx husky-init
cp .husky/pre-commit.example .husky/pre-commit
```

Install NPM dependencies for the client from the main directory with:

```
npm i --prefix src/client
```

#### Server / CLI dependency installation

It is recommended that you install the server / CLI Python packages in a virtual environment. Any will do, but the following are instructions for activating venv:

```
python3 -m venv src/server/venv
source src/server/venv/bin/activate
```

If you intend to run the server / CLI, install the dependencies from requirements.txt:

```
pip install -r src/server/requirements.txt
```

### Running the project

The following instructions can be used to run the Vue client, Flask server, and command-line interface locally.

#### Client

To access the Vue web interface, run from the root directory:

```
cd src/client
npm run dev
```

#### Server

To run the Flask server, activate your virtual environment and run from the root directory:

```
cd src/server
flask --app "server.py" run
```

#### CLI

🚧 CLI setup is currently under development. 🚧

## Development

The following sections include instructions for testing and adding dependencies, for use by developers.

### Testing

Testing frameworks have been set up for project functionality.

#### Server tests

Tests for the Flask server are written with Pytest. It is recommended that you activate your virtual environment first (e.g. venv), then run in the root directory:

```
cd src/server
pytest
```

#### Client tests

Tests for the Vue client are written with Vitest for unit tests, and Playwright for end-to-end tests, the commands for which have been added as `npm` scripts.

Run in the root directory (unit / e2e depending on what is wanted):

```
cd src/client
npm run test:unit
npm run test:e2e
```

Vitest also offers the capability to continuously test and provide immediate feedback as changes are polled through Vite. If you would like this behaviour, change the script in `src/client/package.json` from `"test": "vitest run"` to `"test": "vitest"`. Note that these commands cannot be run as terminal commands.

#### CLI tests

🚧 CLI testing setup is currently under development. 🚧

### Adding dependencies

Follow these steps if you need to add a package during development

#### Adding to client

Packages are added through NPM in the client directory.

For any dependencies that should be there in the production environment, run:

```
npm i <package_name> --save
```

For any dependencies needed for development but not prod (e.g. type checking with ESLint), run:

```
npm i <package_name> --save-dev
```

#### Adding to server / CLI

Packages should be added through `pip` in your virtual environment:

```
pip install <package_name>
pip freeze > requirements.txt
```

## Deployment

### Docker

You can host the client and server locally with Docker. This requires the Docker CLI to be installed with docker compose.

Note that changes to main files (dependencies, settings, etc.) require the containers to be rebuilt.

From the root directory, run:

```
cd src
docker compose up --build
```

⚠️ If using WSL, the docker desktop app must be [installed and configured for WSL](https://docs.docker.com/desktop/wsl/). ⚠️

## Credits

This project is being developed by students of the University of Western Australia (UWA) as part of the unit CITS3200 (Professional Computing), as Team 14 of the 2024 Semester 2 cohort.

Our team members include: Cameron O’Neill, Heidi Leow, Paul Maingi, Ryan Dorman, Shuai Shao, and Vinita Rathore.
