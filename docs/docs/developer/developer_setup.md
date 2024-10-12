# Developer setup

This page provides instructions to get a development client and server up on your machine.

## Installing dependencies

### Git clone

Git clone the repository:

```bash
git clone https://github.com/nlp-tlp/15926-4-RDL-CITS3200.git
```

### Client dependency installation

Download [NVM](https://github.com/nvm-sh/nvm) from the official source or using a package manager for your OS. Then, use NVM to install [NPM](https://nodejs.org/en/download/package-manager).

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

### Server / CLI dependency installation

It is recommended that you install the server / CLI Python packages in a virtual environment. Install the dependencies from requirements.txt:

```bash
pip install -r src/server/requirements.txt
```

## Running the project

#### Client

To access the Vue web interface, run:

```bash
cd src/client
npm run dev
```

Note that the server must be up for the client to access the graph data.

#### Server

To run the Flask server, activate your virtual environment and run:

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
