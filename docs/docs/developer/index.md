# Developer documentation

This section documents the structure and stack of the project code, and setup instructions for developers to work on it.

## Structure of project

### Client

The client is part of the frontend and it provides the static components of the web interface pages. It is also responsible for graph rendering and interactions, for the RDL data queried from the backend.

### Server

The server is part of the backend and is written as a lightweight REST API. It queries and filters the stored RDL data, serving JSON to client requests such that the data is conveniently formatted for frontend rendering.

### Command-line interface

The command-line interface (CLI) part of the backend, and is used as admin access to interact with the server and stored RDL data. It is also responsible for updating the served data from our source of truth for the RDL at https://data.15926.org/rdl.

Note that the CLI and database files are both located under the server folder in the source code, though the CLI was built separately. This is for convenience of deployment.
