# Tech stack

This page describes the main technologies, frameworks and libraries used in the project.

## Frontend

#### Vue.js

[Vue.js documentation](https://vuejs.org/guide/introduction.html)
Vue is a popular Javascript framework for building user interfaces and single-page applications. It is approachable and efficient with easy-to-use reactivity and component-based features.

#### Tailwind

[Tailwind documentation](https://tailwindcss.com/docs/installation)

Tailwind is a CSS framework, that provides low-level classes to building custom designs directly alongside html elements in Javascript frameworks like Vue. Developers can style elements without writing custom CSS, promoting rapid development and a consistent design system.

#### D3.js

[D3.js documentation](https://d3js.org/)

Our frontend graphing makes use of modified D3 tree hierarchy graphs for the main RDL visualisation. D3 is a widely popular graphing library and was chosen for it's flexibility in customisation.

Note that we are not using any variations of D3.js for Vue, just the standard Javascript D3.

## Backend

#### Flask

[Flask documentation](https://flask.palletsprojects.com/en/3.0.x/)

Flask is a lightweight WSGI framework for building web applications and APIs. It is a popular option for building small to medium-sized projects.

#### RDFLib

[RDFLib documentation](https://rdflib.readthedocs.io/en/stable/)

RDFLib is a Python library used for working with RDF (Resource Description Framework) data. It allows for parsing, querying, and serializing RDF graphs, such as the data for the ISO15926 RDL.

## Deployment

#### Docker

[Docker documentation](https://docs.docker.com/)

Docker is an open-source platform that automates the deployment, scaling, and management of applications within lightweight containers. Containers package an application and its dependencies, ensuring consistent environments across different systems.

#### Nginx

[Nginx documentation](https://nginx.org/en/docs/)

Nginx is a high-performance web server for serving static content and handling high-concurrency connections. It is often used to serve web applications and handle web traffic efficiently.

#### Traefik

[Traefik documentation](https://doc.traefik.io/traefik/)

Traefik is a modern reverse proxy and load balancer. It integrates with Docker and other infrastructure to dynamically route traffic, manage SSL certificates, and simplify deployments.

#### Gunicorn

[Gunicorn documentation](https://docs.gunicorn.org/en/stable/)

Gunicorn is a Python WSGI HTTP server for running web applications. It is lightweight, fast, and works well with frameworks like Flask for serving apps in production environments.
