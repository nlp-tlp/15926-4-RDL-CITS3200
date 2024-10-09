## CI/CD

This page describes some of our automatic pipelines run through github for continuous integration / continuous development.

### Auto-deployment to Lightsail

When any code is pushed to the main branch, the code will be automatically deployed to the Lightsail instance. The IP address of the instance and the private key to access it are stored as Github secrets.

The pipeline exports the containers, then uses SSH and secure copy to transfer the containers and any other necessary configuration files and variables. It will also take down the website for up to a few minutes as it replaces the containers and brings the new ones up.

### Client and server linting

Linting pipelines run for the project's source code on pushes to each branch. For the Vue and Typescript code in the frontend, this includes running ESLint and Prettier. For the Python backend we run Black.

### Client and server testing

Testing pipelines run for the project's source code on pushes to each branch. In the frontend, Playwright is used for end-to-end tests, and Vitest is used for unit testing. In the backend, Pytest is used for both unit and integration tests.

The tests for the client and server (and CLI) are in test directories located in their respective source code directories, in /src of the monorepo.
