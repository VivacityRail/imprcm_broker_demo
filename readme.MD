# IMPRCM Broker Demo

This repository contains the demonstration data broker prepared by Vivacity Rail Consulting Ltd for RSSB / XIRCM SG as part of the IMP-RCM project. (c) RSSB 2020.

The repository contains the following:

- folder **design**: the schemas and other design documentation
- folder **broker_demo**: the source code of the data broker, including the test data generator
- folder **doc**: the source text for the web-based documentation suite 


## Design

The main design artefact is the shared schema, held in the spreadsheet `schemas.xlsx`. This holds a master schema and can create derived schemas of various types from it.

## Broker Demo

The broker demo uses Docker Compose. You need to have Docker and Docker Compose installed to run it. See the readme file in the broker_demo folder for details.

The test data generator creates simulated UGMS .csv files matching a specified schema, using 



## Documentation source

This is the source code for the IMP-RCM documentation website. It is built using the Sphinx tool.

