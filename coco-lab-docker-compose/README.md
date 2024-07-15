<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Open Metadata Labs - Using Docker Compose

The open metadata labs contain an interactive environment that allow you to
experiment with different capabilities of Egeria.  More information about the labs can be found at:
[Overview of the Labs](https://egeria-project.org/education/open-metadata-labs/overview/).
The labs are written using Python Jupyter notebooks that
run in a Jupyter Server. The interactive exercises in the notebooks call python functions
that communicate with Egeria. An Apache Kafka server is used by Egeria for communications.

One way to easily deploy a running
Open Metadata Labs environment is by using the Docker Compose scripts contained in this directory.

A docker compose script, coco-lab-setup.yaml uses docker compose to deploy, configure and run a complete working 
environment that includes:

* Three Egeria OMAG Server Platforms (Core, Datalake, and Development)
* Kafka
* Jupyter Server that is used to run the lab excercises


# Getting Started

To get started, you a computer with Docker installed and configured. While most of our experience is running on Mac and 
Linux machines, Windows machines should also work (reach out if you run into issues). 




----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
