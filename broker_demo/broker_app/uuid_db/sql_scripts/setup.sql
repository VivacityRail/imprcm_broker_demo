-- setup of database and users for IMPRCM uuid server database
-- do this as user postgres

CREATE USER imprcm_uuid WITH
  PASSWORD 'imprcm_uuid'
  LOGIN
  NOSUPERUSER
  INHERIT
  CREATEDB
  NOCREATEROLE
  NOREPLICATION;

--GRANT pg_read_server_files to imprcm_demo;

CREATE DATABASE imprcm_demo_uuid_db
    WITH 
    OWNER = imprcm_uuid
    ENCODING = 'UTF8'
    --LC_COLLATE = 'en_GB.UTF-8'
    --LC_CTYPE = 'en_GB.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- reconnect to database imprcm_demo_uuid_db

\c imprcm_demo_uuid_db imprcm_uuid

-- table of UUID schemes. Each scheme represents a category of data for which UUIDs should be generated and could be looked up
CREATE TABLE schemes (
    scheme_url  VARCHAR (80) NOT NULL,
    scheme_name VARCHAR (80) NOT NULL,
    PRIMARY KEY (
        scheme_url
    )
);

-- table of uuids.
CREATE TABLE entities (
    uuid uuid NOT NULL,
    PRIMARY KEY (
        uuid
    )
);

-- table of real-world items which each uuid identifies. This simple structure can handle multiple 
-- names for the same item, as well as names for the same item which change over time.
-- Where the totimestamp column is null, this indicates there is no end date so far known.
CREATE TABLE entity_names (
    entity_id     uuid NOT NULL,
    scheme_id     VARCHAR (80) NOT NULL,
    fromtimestamp VARCHAR (25) NOT NULL,
    name_url      VARCHAR (80) NOT NULL,
    name          VARCHAR (80) NOT NULL,
    totimestamp   VARCHAR (25),
    PRIMARY KEY (
        entity_id,
        scheme_id,
        fromtimestamp
    ),
    FOREIGN KEY (
        scheme_id
    )
    REFERENCES schemes (scheme_url) 
);

-- copy data into the tables from text files
-- (assumes the text files exist)

-- pre-populated for demo with just a single scheme, 'evn' for European Vehicle Number.
insert into schemes (scheme_url, scheme_name) values ('evn', 'European Vehicle Number');
