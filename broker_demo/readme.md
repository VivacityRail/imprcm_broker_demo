# IMP-RCM Prototype Data Broker

## Introduction

This is the source code for the protype data broker built by Vivacity Rail Consulting Ltd for RSSB's IMP-RCM project.

The document comprises the following sections:

- [Functional Description](#functional-description) - a narrative description of the broker.
- [Physical Structure](#physical-structure) - the physical structure of the application.
- [Building the Broker](#building-the-broker) - instructions on how to build the broker from source code using Docker Compose
- [Running the Broker](#running-the-broker) - instructions on how to run the broker using Docker Compose
- [Using the Broker](#using-the-broker) - how to use the broker to load UGMS data and read the results of processing it.
- [Stopping the Broker](#stopping-the-broker) - how to shut down the broker.
- [The Test Data Generator](#test-data-generator) - how to set up and use the Test Data Generator.

## Functional Description

The broker comprises 6 Docker containers which run the code and 2 Docker volumes which contain the databases' data files. Refer to the file `docker-compose.yml` and the Docker Compose documentation at https://docs.docker.com/compose/compose-file/ for details.

The containers are:

- **imprcm_demo_datastore** - a PostgreSQL database holding the loaded and processed data. For this demo, a single database is used for all the processing steps; this needn't be so always.
- **imprcm_demo_uuidstore** - a PostgreSQL database holding a lookup database of identifiers and UUIDs. These are populated using the uuid API described below.
- **imprcm_uuid_api** - a REST-based API for creating and looking up UUIDs for items. It communicates with the the uuid datastore container
- **imprcm_data_loader_ugms** - a polling loader which looks for incoming UGMS data files in the correct broker .csv format and loads them to a touchdown database. The files may be zipped up in the .gz format.
- **imprcm_ugms_pipeline** - a polling processor which looks for newly-loaded UGMS data files and processes them through a pipeline, putting the results into a queryable data table.
- **imprcm_sandc_api** - a REST-based API for querying summary information on the UGMS data gathered for S&C units.

The volumes are:

- **imprcm_data_store** - the database in which the UGMS data is stored
- **imprcm_uuid_store** - the database in which the UUID lookup data is stored.

The application also sets up an inbox folder into which it expects incoming UGMS .csv files to be placed.

## Physical Structure

### Data stores
The two data store containers are PostgreSQL databases, accessed via TCP/IP on the cluster's internal network using standard PostgreSQL methods. The databases can be accessed from outside the cluster using normal PostgreSQL tools, on ports defined at runtime. See [Running the Broker](#running-the-broker) below for more on ports.

The UUID Server data store is defined by the script `broker_demo/broker_app/uuid_db/sql_scripts/setup.sql`.

The UGMS data store is defined by the script `broker_demo/broker_app/data_store/sql_scripts/setup.sql`.


### APIs
The two APIs are hosted using the `Flask` Python-based web server, with the `connexion` add-on which allows the API to be defined using a Swagger file. The relevant file is held within the container's folder structure in the `swagger.yml` file in the `swagger` folders:
- for the uuid API - `broker_demo/broker_app/uuid_server/imprcm_uuid_server/swagger`
- for the outbound S&C API `broker_demo/broker_app/outbound_api/imprcm_query_server/swagger`


### Code - data loader
The data loader is a Python program which uses the PostgreSQL fast loader to load the .csv files to the database. As well as loading the files, it maintains a list of files that have been loaded in a database table.

The code is in the folder `broker_demo/broker_app/inbound_ugms/ugms_file_loader`.

### Code - processing pipeline
The processing pipeline is a Python program which polls the files-loaded table for new files and processes the data loaded from them by issuing SQL statements to the PostgreSQL database. It keeps track of the files for which it has processed the data.

The code is in the folder `broker_demo/broker_app/processing_pipeline/python_processor`.

## Building the Broker

The broker is built simply by opening a command, powershell or bash window in the folder that contains the `docker-compose.yml` file (`broker_demo/broker_app`) and issing the Docker Compose command `docker-compose build`. This rebuilds all the containers from source if they have changed since the last build.

## Running the Broker

To run the broker, issue the Docker Compose command `docker-compose up`.  The command looks for environment variables to set the TCP ports on which the various elements can be accessed on the host on which the broker is running. All have default values, so the broker will run correctly on the default ports if you don't specify the environment variables:

- PORT_UUAPI (default 8080): the port on which the UUID API can be accessed via http.
- PORT_OBAPI (default 8085): the port on which the outbound S&C data API can be accessed via http.
- PORT_UDB (default 5433): the port on which the UUID database can be accessed via PostgreSQL.
- PORT_SDB (default 5432): the port on which the UGMS database can be accessed via PosgreSQL.

There are several ways you can set these variables for the broker to pick up:
- in the command shell before you run the broker. If on linux, use `EXPORT <variable>`; if in powershell, use `$env:<variable>`; if in Windows command, use `set <variable>`.
- on the command line to the `docker compose run` command, using the `-e variable` option. You will need to issue the `run` command for each of the containers separately for this to work.
- by putting them in a `.env` file in the same folder as `docker-compose.yml`.

When run using `docker-compose up`, the broker generates log messages in the same shell session and will run until you stop it by pressing control-C.

You can also run using `docker-compose up -d`, which runs in the background so the shell prompt returns immediately.

Note that you may need to clear away any previous incarnations of the data volumes if you wish to start from scratch. Use `docker volume ls` to list volumes and `docker volume rm <vol>` to remove. **NOTE THAT REMOVING A VOLUME DELETES ALL DATA IN IT** so you will be starting with empty databases.

### Loading UGMS files
You can create valid UGMS data files from vendor-specific ones using one of the Python data adapters such as `create_imprcm_format_ugms_csv_from_swt.py` in the `input_adapters` folder; and you can generate these files if necessary using the Test Data Generator (described below). 

Copy files (whether zipped up or not) into the folder `inbound_ugms/data/inbox`. The loader will pick them up and load them to the touchdown table in the PostgreSQL database. You can track progress by logging in to the  database using any standard tool and querying the `files_loaded` table. (We used pgAdmin https://www.pgadmin.org/ - other tools are available and PostgreSQL comes with its own commnand-line query tool `psql`.)

The loaded files will be deleted from the inbox.

The processing pipeline will automatically be triggered by the presence of new data; and after a short pause the new summary data will appear in the output table and be available to the outbound API

### Using the outbound S&C API
You can query this API using a web browser or any web-connecting tool, on the port specified at runtime or 8085. There is a sample application in the `excel_client` folder which uses MS-Excel to query using the API and populate a data table.

The specification of the API and so the valid requests to it are in the file `swagger.yaml` in the `outbound_api` folder tree.

You can browse the Swagger-generated documentation on the `/ui` endpoint of your host and outbound API port - e.g. `http://localhost:8085/ui`

### Using the UUID API
You can query this API using a web browser or any web-connecting tool, on the port specified at runtime or 8080. The API is specified using the `swagger.yaml` file in the `uuid_server` folder tree. 

You can browse the Swagger-generated documentation on the `/ui` endpoint of your host and uuid API port - e.g. `http://localhost:8080/ui`

## Stopping the Broker
To stop the broker, type control-C at the command line, or if you ran the broker using the "detached" option `-d`, issue the Docker Compose command `docker-compose down`.

## Test Data Generator
The Test Data Generator is a Python program that generates sample UGMS files. It uses a SQLite database to hold details of the track geography, basic track geometry pattern and train timetable to use. The generator and associated database files and scripts are held in the folder `broker_demo/ugms_test_data_gen`.


### The SQLite Database
The Test Generator connects to a SQLite database specified on the command line. The database contains a set of linked tables which are populated with data to represent the track geography, the train timetable, the track geometry readings and the rolling stock units involved. An overlay table allows dated changes to the geometry to be superimposed, to simulate degradation or repair of sections of track over time.

The script `create_db.sql` creates the tables and also contains SQLite commands to populate them by reading .csv files. Samples of these .csv files can be found in the `UGMS Test Data Generator/data/development` folder.

The database contains a table which records the last simulated odometer ("tacho") reading for each rolling stock unit. This is read at the start of each run so that the odometer reading increments over the runs. It can be pre-populated if necessary with starting odometer readings.

### Command line parameters
The generator expects the name of a SQLite database on the command line. It can also take some additional named parameters:

- `debug`: if included, this limits the size of the output file to a small time duration (set by the constant DEBUG_SECONDS in the Python program). It is useful for testing the generator to ensure that the SQLite database has been correctly set up.
- `unit`: the name of the rolling stock unit to create a file for. If this is omitted, files will be generated for all the units listed in the SQLite database
- `rundate`: the date to create the files for. If omitted, the current date will be used.
- `deptime`: the train departure time to create a file for. If omitted, all the trains run by the specified unit(s) will be included
- `trainid`: the train ID to create the file for. If omitted, all the trains run by the specified unit(s) will be included.

### Scripting the generator
The Test Data Generator is most easily run using a script such as a Powershell script or batch file. A sample Powershell script `Run_test.generator.ps1` can be found in the folder. This script reads a text file - the "scenario file" - containing a list of SQLite databases, simulated dates of operation and UGMS units to generate files for in each run of the generator. It also zips up the files it creates using the 7zip utility - this should be installed. Note that these scripts only work on a Windows host - there are no Linux equivalents.

### Live generator

In the folder `broker_demo/ugms_test_data_gen/live` is an experimental live data generator. This reads a previously-generated test data file and emits its rows of data in pseudo-real time, as if the data were being live-transmitted back from a running train. It would be possible to connect this to, for example, a `stomp` server to broadcast the live data.
