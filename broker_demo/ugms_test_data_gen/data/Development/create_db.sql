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
	lefttop35m real,
	righttop35m	real,
	meantop70m real,
	gaugemm real,
	crosslevel real,
	twist3m real,
	curvature real,
	cyclictop real,
	dipanglem real
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
	lefttop35m real,
	righttop35m	real,
	meantop70m real,
	gaugemm real,
	crosslevel real,
	twist3m real,
	curvature real,
	cyclictop real,
	dipanglem real
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

-- load basic data from .csv files
-- note that files must have no headers if going to an existing table
.mode csv

-- geog
.import geog_train_data.csv geog_train
select 'geog', count(*) from geog_train;

-- geom
.import default_geom_data.csv default_geom
select 'geom', count(*) from default_geom;

.import geom_overlay_data.csv geom_overlay
select 'overlay', count(*) from geom_overlay;

-- tt
.import tt_data.csv tt
select 'tt', count(*) from tt;







	