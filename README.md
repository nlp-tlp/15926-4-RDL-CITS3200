# 15926-4-RDL-CITS3200

## Visualisation of the ISO 15926-4 Reference Data Library

## Overview
This project aims to develop an interactive visualisation for an equipment reference data library as described in the ISO 15926-4 Standard. The goal is to create a web-based interface that allows users to interrogate the data and visualise the hierarchical relations.

## Purpose
The current browser, https://data.15926.org/rdl/, is frustrating to use due to the lack of hierarchical visualisation. This project aims to enhance the user experience and improve data accessibility.


## Setup (Development)
This project uses a mix of pre-commit checks and github actions in the workflow, ensuring clean code. To properly setup the project follow these steps.

### Clone the repositry
  `git clone https://github.com/nlp-tlp/15926-4-RDL-CITS3200.git`

### Install dependencies
  `./setup.sh` (Do not run with `sudo`)

### Build and run Docker containers
`cd src`

`docker compose up --build`

- Note: Any changes to main files (dependencies, settings, etc.) require the containers to be rebuilt.