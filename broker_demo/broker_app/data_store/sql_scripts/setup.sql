-- setup of database and users for IMPRCM broker data store container

-- do this as user postgres

CREATE USER imprcm_demo WITH
  PASSWORD 'imprcm_demo'
  LOGIN
  NOSUPERUSER
  INHERIT
  CREATEDB
  NOCREATEROLE
  NOREPLICATION;

--GRANT pg_read_server_files to imprcm_demo;

CREATE DATABASE imprcm_demo_ugms_touchdown
    WITH 
    OWNER = imprcm_demo
    ENCODING = 'UTF8'
    --LC_COLLATE = 'en_GB.UTF-8'
    --LC_CTYPE = 'en_GB.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- reconnect to database imprcm_demo_ugms_touchdown

\c imprcm_demo_ugms_touchdown imprcm_demo


-- reference tables

-- reference list of Switch and Crossing units. This is populated for the demo with a list from 
-- Ellipse for the section of track from Paddington to Reading.
 CREATE TABLE s_and_c_reference
( main_elr varchar(4)
, main_track_id varchar(4)
, from_miles_pt_yards real
, to_miles_pt_yards real
, length_miles_pt_yards real
, unit_type varchar(2)
, description varchar(255)
, second_elr varchar(4)
, second_tid varchar(4)
, from_miles_pt_yards_2 real
, to_miles_pt_yards_2 real
, length_yards_2 real
, vertical_or_inclined varchar(1)
, unit_year varchar(4)
, sleeper_or_baseplate varchar(20)
, fastening varchar(1)
, fixing varchar(1)
, check_rail varchar(1)
, ballast_method varchar(1)
, unique_id varchar(10)
, item_number real
, letter varchar(1)
, alloy_left varchar(1)
, alloy_right varchar(1)
, switch_blade varchar(1)
, left_year varchar(2)
, left_new_or_serv varchar(1)
, right_year varchar(2)
, right_new_or_serv varchar(1)
, direction varchar(1)
, s_and_t_number varchar(10)
, switch_type varchar(1)
, switch_angle real
, switch_hand varchar(1)
, switch_alloy varchar(1)
, perm_speed_restriction_mph real
, main_from_m real
, main_to_m real
, second_from_m real
, second_to_m real
-- offsets when travellng in increasing mileage direction
, main_forward_offset_start_m real
, main_forward_offset_end_m real
, main_forward_offset_mid_m real
, main_forward_offset_switch_m real
, second_forward_offset_start_m real
, second_forward_offset_end_m real
, second_forward_offset_mid_m real
, second_forward_offset_switch_m real
-- offsets in decreasing mileage direction, from defined end point
, main_reverse_offset_start_m real
, main_reverse_offset_end_m real
, second_reverse_offset_start_m real
, second_reverse_offset_end_m real
, main_reverse_offset_mid_m real
, main_reverse_offset_switch_m real
, second_reverse_offset_mid_m real
, second_reverse_offset_switch_m real
, s_and_c_uuid uuid
);

-- simple historic train timetable with basic train information 
-- and allocated rolling stock
CREATE TABLE timetable_reference(
 unit varchar(20)
, trainid varchar(8)
, deptime time
, arrtime time
, from_tiploc varchar(7)
, to_tiploc varchar(7)
, direction integer
, diagram varchar(4)
)
;

-- list of S&C units wanted for extract to the summary data table.
-- In the demo this is restricted to those for which we have geometry data.
CREATE TABLE wanted_s_and_cs
(
    unique_id character varying(10)  NOT NULL,
    CONSTRAINT wanted_s_and_cs_pkey PRIMARY KEY (unique_id)
);


-- transactional data tables

-- list of inbound ugms data files loaded and processed
CREATE TABLE files_loaded
(
    file_name character varying(255) ,
    loaded_timestamp timestamp without time zone,
    processed_to_s_and_c_timestamp timestamp without time zone,
    summarised_timestamp timestamp without time zone,
    archived_timestamp timestamp without time zone,
    file_uuid uuid,
    rowcount bigint,
    status character varying(20)
);

-- touchdown table into which data from ugms csv files are loaded.
-- the scheme for this table matches the imp-rcm format csv file structure
CREATE TABLE ugms_touchdown
(
    file_timestamp_utc timestamp without time zone NOT NULL,
    file_name character varying(255) NOT NULL,
    file_uid uuid NOT NULL,
    extended_items_metadata text,
    timestamp_recorded_utc timestamp without time zone NOT NULL,
    extended_items_time text ,
    ugms_unit_id character varying(100)  NOT NULL,
    ugms_unit_uid uuid NOT NULL,
    gps_fix_quality real,
    gps_latitude_deg real,
    gps_longitude_deg real,
    speed_as_recorded real,
    speed_as_recorded_unit character varying(20),
    elapsed_distance_as_recorded_m real,
    extended_items_geography text,
    left_top_35m_mm real,
    right_top_35m_mm real,
    crosslevel_mm real,
    twist_3m_mm real,
    left_top_35m_sd_mm real,
    right_top_35m_sd_mm real,
    mean_top_70m_sd_mm real,
    twist_3m_sd_mm real,
    left_dip_joint_mrad real,
    right_dip_joint_mrad real,
    pseudo_align_35m_mm real,
    pseudo_align_70m_mm real,
    pseudo_align_35m_sd_mm real,
    pseudo_align_70m_sd_mm real,
    mean_top_70m_mm real,
    extended_items_geometry text,
    accel_z_wb_ms_2 real,
    accel_x_wc_ms_2 real,
    accel_x_wd_ms_2 real,
    accel_y_wd_ms_2 real,
    accel_y_wp_ms_2 real,
    data_row_uid uuid NOT NULL,
    creating_adapter_version character varying(40) NOT NULL
);


-- extracted and processed ugms data on S&C units. This is filtered by distance and running line
-- so that it covers the S&C unit and a length of plain line either side.
-- The table is populated by the processing pipeline script
CREATE TABLE ugms_s_and_c
(
    file_uid uuid NOT NULL,
    extended_items_metadata text,
    timestamp_recorded_utc timestamp without time zone NOT NULL,
    extended_items_time text,
    ugms_unit_id character varying(100) NOT NULL,
    ugms_unit_uid uuid NOT NULL,
    gps_fix_quality real,
    gps_latitude_deg real,
    gps_longitude_deg real,
    speed_as_recorded real,
    speed_as_recorded_unit character varying(20),
    elapsed_distance_as_recorded_m real,
    extended_items_geography text,
    left_top_35m_mm real,
    right_top_35m_mm real,
    crosslevel_mm real,
    twist_3m_mm real,
    left_top_35m_sd_mm real,
    right_top_35m_sd_mm real,
    mean_top_70m_sd_mm real,
    twist_3m_sd_mm real,
    left_dip_joint_mrad real,
    right_dip_joint_mrad real,
    pseudo_align_35m_mm real,
    pseudo_align_70m_mm real,
    pseudo_align_35m_sd_mm real,
    pseudo_align_70m_sd_mm real,
    mean_top_70m_mm real,
    extended_items_geometry text,
    accel_z_wb_ms_2 real,
    accel_x_wc_ms_2 real,
    accel_x_wd_ms_2 real,
    accel_y_wd_ms_2 real,
    accel_y_wp_ms_2 real,
    data_row_uid uuid NOT NULL,
    creating_adapter_version character varying(40) NOT NULL,
    unique_id character varying(10),
    offset_along_s_and_c_m real,
    direction_of_travel integer,
    main_elr character varying(4),
    main_track_id character varying(4),
    miles_decimal real,
    miles_plus_yards character varying(10),
    miles_cln_chains character varying(6)
);

-- summary data for the wanted S&C units, summarised from the ugms_s_and_c table
-- by the processing pipeline script
CREATE TABLE ugms_s_and_c_summary
(
    sample_date date,
    left_top_35m_sd_mm real,
    right_top_35m_sd_mm real,
    mean_top_70m_sd_mm real,
    twist_3m_sd_mm real,
    pseudo_align_35m_sd_mm real,
    pseudo_align_70m_sd_mm real,
    unique_id character varying(10),
    direction_of_travel integer,
    main_elr character varying(4),
    main_track_id character varying(4),
    miles_decimal_from real,
    miles_plus_yards_from character varying(10),
    miles_cln_chains_from character varying(6),
    miles_decimal_to real,
    miles_plus_yards_to character varying(10),
    miles_cln_chains_to character varying(6)
);



-- copy data into the tables from text files
-- (assumes the text files exist)

\copy wanted_s_and_cs FROM '/docker-entrypoint-initdb.d/wanted_s_and_cs.txt'
\copy timetable_reference FROM '/docker-entrypoint-initdb.d/timetable_reference.txt'
\copy s_and_c_reference FROM '/docker-entrypoint-initdb.d/s_and_c_reference.txt' 

-- temporary just to test the outbound interface
\copy ugms_s_and_c_summary FROM '/docker-entrypoint-initdb.d/ugms_s_and_c_summary.txt' 