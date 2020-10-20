@echo off
rem populate otgm_test_2 database with basic train, geog, geom data, then generate simulated OTGM csv
rem assumes sqlite3 is on the path.
rem requires geog_train_data.csv, default_geom_data.csv and tt_data.csv

rem optionally could use geom_overlay_data.csv for geometry overlays

rem create and populate the database
rem sqlite3 otgm_test.db < create_db_SWT.sql

sqlite3 SC_test.db < create_db_SWT.sql

rem run sql script to create output data and pass into csv file
rem note this file has nealry 300,000 rows and is 32Mb in size
sqlite3 SC_test.db < generate_track_geometry.sql > T1001_20180616_geom.csv