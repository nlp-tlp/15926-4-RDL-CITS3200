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

These instructions will [install dependencies](#installing-dependencies) get a copy of the project [up and running](#running-the-project) on your local machine.

### Installing dependencies

This project consists of a Vue client, Flask server, and command-line interface. Dependencies must first be installed before running any of these.

#### Git clone

Git clone the repository:

```bash
git clone https://github.com/nlp-tlp/15926-4-RDL-CITS3200.git
```

#### Client dependency installation

If you intend to run the client, download [NVM](https://github.com/nvm-sh/nvm) from the official source or using a package manager for your OS. Then, use NVM to install [NPM](https://nodejs.org/en/download/package-manager).

Install NPM dependencies in the main directory for [Husky Git hooks](https://typicode.github.io/husky/) and initialise Husky:

```bash
npm i
npx husky-init
cp .husky/pre-commit.example .husky/pre-commit
```

Install NPM dependencies for the client from the main directory with:

```bash
npm i --prefix src/client
```

#### Server / CLI dependency installation

It is recommended that you install the server / CLI Python packages in a virtual environment. Install the dependencies from requirements.txt:

```bash
pip install -r src/server/requirements.txt
```

### Running the project

The following instructions can be used to run the Vue client, Flask server, and command-line interface locally for development.

#### Client

To access the Vue web interface, run from the root directory:

```bash
cd src/client
npm run dev
```

#### Server

To run the Flask server, activate your virtual environment and run from the root directory:

```bash
cd src/server
flask --app "server.py" run
```

#### CLI

To run the CLI for the Flask server:

```bash
cd src/server
./cli.py
```

Follow the directions given in the CLI menu to modify the database and view other parameters.

## Development

The following sections include instructions for testing and adding dependencies, for use by developers.

### Testing

Testing frameworks have been set up for project functionality.

#### Server tests

Tests for the Flask server and CLI are written with Pytest. It is recommended that you activate your virtual environment first (e.g. venv), then run in the root directory:

```bash
cd src/server
pytest
```

#### Client tests

Tests for the Vue client are written with Vitest for unit tests, and Playwright for end-to-end tests, the commands for which have been added as `npm` scripts.

Run in the root directory (unit / e2e depending on what is wanted):

```bash
cd src/client
npm run test:unit
npm run test:e2e
```

Vitest also offers the capability to continuously test and provide immediate feedback as changes are polled through Vite. If you would like this behaviour, change the script in `src/client/package.json` from `"test": "vitest run"` to `"test": "vitest"`. Note that these commands cannot be run as terminal commands.

### Adding dependencies

Follow these steps if you need to add a package during development

#### Adding to client

Packages are added through NPM in the client directory.

For any dependencies that should be there in the production environment, run:

```bash
npm i <package_name> --save
```

For any dependencies needed for development but not prod (e.g. type checking with ESLint), run:

```bash
npm i <package_name> --save-dev
```

#### Adding to server / CLI

Packages should be added through `pip` in your virtual environment:

```bash
pip install <package_name>
pip freeze > requirements.txt
```

## Deployment

### Docker

You can host the client and server locally with Docker. This requires the Docker CLI to be installed with docker compose.

Note that changes to main files (dependencies, settings, etc.) require the containers to be rebuilt.

From the root directory, run:

```bash
cd src
docker compose up --build
```

⚠️ If using WSL, the docker desktop app must be [installed and configured for WSL](https://docs.docker.com/desktop/wsl/). ⚠️

#### Running the CLI

To access the CLI inside of the docker container, run :

```bash
docker exec -it Server /app/cli.py
```

## Credits

This project is being developed by students of the University of Western Australia (UWA) as part of the unit CITS3200 (Professional Computing), as Team 14 of the 2024 Semester 2 cohort.

Our team members include: Cameron O’Neill, Heidi Leow, Paul Maingi, Ryan Dorman, Shuai Shao, and Vinita Rathore.
