![CI](https://github.com/terra-store/terra-store/actions/workflows/build.yml/badge.svg) ![CodeQL](https://github.com/terra-store/terra-store/workflows/CodeQL/badge.svg) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/02ce2a63a46e4b28aea65c866c4ea932)](https://www.codacy.com/gh/terra-store/terra-store/dashboard?utm_source=github.com&utm_medium=referral&utm_content=terra-store/terra-store&utm_campaign=Badge_Grade)  [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/02ce2a63a46e4b28aea65c866c4ea932)](https://www.codacy.com/gh/terra-store/terra-store/dashboard?utm_source=github.com&utm_medium=referral&utm_content=terra-store/terra-store&utm_campaign=Badge_Coverage) [![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Terra-Store

Terra-Store is an open source implementation of the terraform registry api for modules and providers

It is currently in an early development phase with only a dummy backend supported.

## Project Status

### Milestone 1 - Project Setup and basic modules API implementation

The goals of the project in the first milestone are as follows:

-   [x] Establish Repositories and projects in Github
-   [ ] Setup basic Open Source Documentation and practices
-   [x] Create Extended modules API 
-   [x] Establish CI and Code Quality for the project
-   [x] Implement Unit test patterns
-   [x] Implement Integration Test patterns
-   [ ] Automated tests using terraform cli (fully integrated tests) - 0.15.3
-   [ ] Document processes to make project easier for future contributers
-   [ ] Add extensible backend system, implement filesystem only in M1
-   [ ] Add yaml configuration system

### Milestone 3 - Providers API and S3 Backend

## Build Instrictions

The project is using make to simplify the local build and CI build process

### Prequisites

-   Make
-   Python 3.6+
-   pip
-   virtualenv

1.  Before commencing make sure you have installed tohe items listed above.
2.  create a python virtualenv: `python3 -m venv venv`
3.  Activate the viurtual env: `source venv/bin/activate`

### Building and Testing

All build and test commands are invoked by running: `make <target>`

### Supported targets

| Target     | Description                                     |
| ---------- | ----------------------------------------------- |
| build      | Builds the terra-store wheel                    |
| clean      | Clean up build artifacts                        |
| help       | Display this help text                          |
| production | Build production container                      |
| prod-run   | Runs production container with port 8080 mapped |
| run        | Run local version of flask app                  |
| test       | Run all test packages                           |
