-- SQLite sql script for tables creation and population from csv

DROP TABLE IF EXISTS geog_train;
CREATE TABLE geog_train (
	fromloc text,
	toloc text,
	seconds integer,
	metres real,
	metres_to real,
	speedmpers real,
	accelmperspers real,
	latitude real,
	latdirection integer,
	longitude real,
	longdirection integer,
	kminmetres real,
	offsetmstart real,
	offsetmend real
	)
;

DROP TABLE IF EXISTS default_geom;
CREATE TABLE default_geom (
    offsetm real,
	accel_z_wb_ms_2 real,
	accel_x_wc_ms_2 real,
	accel_x_wd_ms_2 real,
	accel_y_wd_ms_2 real,
	accel_y_wp_ms_2 real,
	right_dip_joint_mrad real,
	left_dip_joint_mrad real,
	left_top_35m_mm real,
	right_top_35m_mm real,
	mean_top_70m_mm real,
	pseudo_align_35m_mm real,
	pseudo_align_70m_mm real,
	crosslevel_mm real,
	twist_3m_mm real,
	curvature_mm real,
	left_top_35m_sd_mm real,
	right_top_35m_sd_mm real,
	mean_top_35m_sd_mm real,
	pseudo_align_35m_sd_mm real,
	pseudo_align_70m_sd_mm real,
	twist_3m_sd_mm real
)

;

DROP TABLE IF EXISTS tt;
CREATE TABLE tt (
	unit text,
	trainid text,
	deptime text,
	fromloc text,
	toloc text
)
;
DROP TABLE IF EXISTS tacho;
CREATE TABLE tacho (
	unit text,
	last_tacho int
)
;
INSERT INTO tacho (unit, last_tacho)
VALUES ('A', 012345678);
INSERT INTO tacho (unit, last_tacho)
VALUES ('B', 56789012);
INSERT INTO tacho (unit, last_tacho)
VALUES ('C', 90123456);


DROP TABLE IF EXISTS geom_overlay;
-- overlay of geometry data for given from / to locations and start position in metres, for given date range

-- use this to create specific test cases for geometry
CREATE TABLE geom_overlay (
	fromdate text,
	todate text,
	fromloc text,
	toloc text,
	startm real, 
	accel_z_wb_ms_2 real,
	accel_x_wc_ms_2 real,
	accel_x_wd_ms_2 real,
	accel_y_wd_ms_2 real,
	accel_y_wp_ms_2 real,
	right_dip_joint_mrad real,
	left_dip_joint_mrad real,
	left_top_35m_mm real,
	right_top_35m_mm real,
	mean_top_70m_mm real,
	pseudo_align_35m_mm real,
	pseudo_align_70m_mm real,
	crosslevel_mm real,
	twist_3m_mm real,
	curvature_mm real,
	left_top_35m_sd_mm real,
	right_top_35m_sd_mm real,
	mean_top_35m_sd_mm real,
	pseudo_align_35m_sd_mm real,
	pseudo_align_70m_sd_mm real,
	twist_3m_sd_mm real	
)
;


-- view to generate basic geometry (no overlay)
DROP VIEW IF EXISTS v_basic_geometry_test;
CREATE VIEW v_basic_geometry_test
AS
SELECT
	tt.unit,
	tt.trainid,
	tt.fromloc,
	tt.toloc,
	tt.deptime,
	geog.speedmpers,
	geog.accelmperspers,
	datetime(julianday(date('now')||' '||tt.deptime) + geog.seconds / 86400.0) gpstimestamp,
	geog.latitude,
	geog.longitude,
	geog.kminmetres + geom.offsetm metres,
	10220323 + cast(30 * (geog.kminmetres + geom.offsetm) as int) tacho,
	geom.gaugemm
FROM tt
INNER JOIN geog_train geog 
ON geog.fromloc = tt.fromloc
AND geog.toloc = tt.toloc
INNER JOIN default_geom geom
ON geom.offsetm BETWEEN geog.offsetmstart AND geog.offsetmend
;

-- view to include lengthy query parts from test generator
DROP VIEW IF EXISTS v_test_generator_query;
CREATE VIEW v_test_generator_query
AS
SELECT
	tt.unit,
	tt.trainid, 
	tt.fromloc, 
	tt.deptime, 
	geog.speedmpers, 
	geog.latitude, 
	geog.longitude, 
	geog.seconds, 
COALESCE (overlay.left_top_35m_mm, geom.left_top_35m_mm ),
COALESCE (overlay.right_top_35m_mm, geom.right_top_35m_mm ),
COALESCE (overlay.mean_top_70m_mm, geom.mean_top_70m_mm ),
COALESCE (overlay.pseudo_align_35m_mm, geom.pseudo_align_35m_mm ),
COALESCE (overlay.pseudo_align_70m_mm, geom.pseudo_align_70m_mm ),
COALESCE (overlay.crosslevel_mm, geom.crosslevel_mm ),
COALESCE (overlay.twist_3m_mm, geom.twist_3m_mm ),
COALESCE (overlay.curvature_mm, geom.curvature_mm ),
COALESCE (overlay.right_dip_joint_mrad, geom.right_dip_joint_mrad ),
COALESCE (overlay.left_dip_joint_mrad, geom.left_dip_joint_mrad ),
COALESCE (overlay.timestamp_ticks, geom.timestamp_ticks ),
COALESCE (overlay.master_sync_inc, geom.master_sync_inc ),
COALESCE (overlay.master_sync_state, geom.master_sync_state ),
COALESCE (overlay.tacho, geom.tacho ),
COALESCE (overlay.flags, geom.flags ),
COALESCE (overlay.speed_mph, geom.speed_mph ),
COALESCE (overlay.accel_z_wb_ms_2, geom.accel_z_wb_ms_2 ),
COALESCE (overlay.accel_x_wc_ms_2, geom.accel_x_wc_ms_2 ),
COALESCE (overlay.accel_x_wd_ms_2, geom.accel_x_wd_ms_2 ),
COALESCE (overlay.accel_y_wd_ms_2, geom.accel_y_wd_ms_2 ),
COALESCE (overlay.accel_y_wp_ms_2, geom.accel_y_wp_ms_2 ),
COALESCE (overlay.reserved, geom.reserved ),
COALESCE (overlay.elapsed_distance_km, geom.elapsed_distance_km ),
COALESCE (overlay.left_top_35m_SD, geom.left_top_35m_SD ),
COALESCE (overlay.right_top_35m_SD, geom.right_top_35m_SD ),
COALESCE (overlay.mean_top_35m_SD, geom.mean_top_35m_SD ),
COALESCE (overlay.pseudo_align_35m_SD, geom.pseudo_align_35m_SD ),
COALESCE (overlay.pseudo_align_35m_SD, geom.pseudo_align_35m_SD ),
COALESCE (overlay.twist_3m_SD, geom.twist_3m_SD ),
COALESCE (overlay.gps_fix_quality, geom.gps_fix_quality ),
COALESCE (overlay.gps_latitude_deg, geom.gps_latitude_deg ),
COALESCE (overlay.gps_longitude_deg, geom.gps_longitude_deg )
FROM tt 
INNER JOIN geog_train geog 
ON geog.fromloc = tt.fromloc AND geog.toloc = tt.toloc 
INNER JOIN default_geom geom 
ON geom.offsetm BETWEEN geog.offsetmstart AND geog.offsetmend 
LEFT OUTER JOIN geom_overlay overlay
ON overlay.startm = (geog.kminmetres + geom.offsetm) AND :rundate BETWEEN overlay.fromdate and overlay.todate 
;

-- load basic data from .csv files
-- note that files must have no headers if going to an existing table
.mode csv

-- geog
.import geog_train_data.csv geog_train
select 'geog', count(*) from geog_train;

-- geom
.import default_geom_data_SWT.csv default_geom
select 'geom', count(*) from default_geom;

.import geom_overlay_data_SWT.csv geom_overlay
select 'overlay', count(*) from geom_overlay;

-- tt
.import tt_data.csv tt
select 'tt', count(*) from tt;







	