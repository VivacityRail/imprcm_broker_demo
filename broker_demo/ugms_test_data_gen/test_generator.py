import sys
import sqlite3
import pandas as pd
import pandas.io.sql as sql
import argparse
import logging
import tempfile, shutil, os
from datetime import datetime 

'''
    Test generator, as a module.
	Usage in python:
	>>>from test_generator_module import create_csv
	>>>create_csv(['database.db', '--unit=C', '--rundate=20171231', '--debug'])

    or whatever you need the parameters to be	
    
    This version of the test generator creates output files compliant with SWT UGMS format

'''
#testing 123
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

CHUNKSIZE = 200000
DEBUG_SECONDS = 81
#version with extra tables for checking. Include columns in query too.
#SWT_OUTPUT_COLUMNS = [ 'timestamp_ticks', 'speedmpers', 'offsetm', 'metres', 'seconds', 'master_sync_inc', 'master_sync_state', 'tacho', 'flags', 'speed_mph', 'accel_z_wb_ms_2', 'accel_x_wc_ms_2', 'accel_x_wd_ms_2', 'accel_y_wd_ms_2', 'accel_y_wp_ms_2', 'reserved', 'right_dip_joint_mrad', 'left_dip_joint_mrad', 'left_top_35m_mm', 'right_top_35m_mm', 'mean_top_70m_mm', 'pseudo_align_35m_mm', 'pseudo_align_70m_mm', 'crosslevel_mm', 'twist_3m_mm', 'curvature_mm', 'elapsed_distance_km', 'left_top_35m_SD_mm', 'right_top_35m_SD_mm', 'mean_top_35m_SD_mm', 'pseudo_align_35m_SD_mm', 'pseudo_align_70m_SD_mm', 'twist_3m_SD_mm', 'gps_fix_quality', 'gps_latitude_deg', 'gps_longitude_deg' ]
#SWT_HEADER_ROW1 = 'DataReaderWriter, Version=1.2.700.0,Geometry,{0},,BBRL.UTGMS.CommonUtilities.DataTypes.FloatDataSampleSet'
#SWT_HEADER_ROW2 = 'Time Stamp,Speed,Offsetm,Metres, Seconds, Master Sync Inc,Master Sync State,Tacho,"AccelZ_Wb Invalid,AccelX_Wc Invalid,AccelX_Wd Invalid,AccelY_Wd Invalid,AccelY_Wp Invalid,Reserved Invalid,Right Dipped Joint Invalid,Left Dipped Joint Invalid,Left Top 35m Invalid,Right Top 35m Invalid,Mean Top 70m Invalid,Pseudo Align 35m Invalid,Pseudo Align 70m Invalid,Crosslevel Invalid,Twist 3m Invalid,Curvature Invalid,FQU|Fix Quality Invalid,LAS|Latitude Invalid,LOS|Longitude Invalid",Speed |MPH,AccelZ_Wb|m/s2,AccelX_Wc|m/s2,AccelX_Wd|m/s2,AccelY_Wd|m/s2,AccelY_Wp|m/s2,Reserved|N/A,Right Dipped Joint|mrads,Left Dipped Joint|mrads,Left Top 35m|mm,Right Top 35m|mm,Mean Top 70m|mm,Pseudo Align 35m|mm,Pseudo Align 70m|mm,Crosslevel|mm,Twist 3m|mm,Curvature|mm,Distance |km,Left Top 35m SD,Right Top 35m SD,Mean Top 70m SD,Pseudo Align 35m SD,Pseudo Align 70m SD,Twist 3m SD,FQU|Fix Quality,LAS|Latitude,LOS|Longitude'

#version without extra tables for checking. Exclude columns in query too.
SWT_OUTPUT_COLUMNS = [ 'timestamp_ticks', 'master_sync_inc', 'master_sync_state', 'tacho', 'flags', 'speed_mph', 'accel_z_wb_ms_2', 'accel_x_wc_ms_2', 'accel_x_wd_ms_2', 'accel_y_wd_ms_2', 'accel_y_wp_ms_2', 'reserved', 'right_dip_joint_mrad', 'left_dip_joint_mrad', 'left_top_35m_mm', 'right_top_35m_mm', 'mean_top_70m_mm', 'pseudo_align_35m_mm', 'pseudo_align_70m_mm', 'crosslevel_mm', 'twist_3m_mm', 'curvature_mm', 'elapsed_distance_km', 'left_top_35m_SD_mm', 'right_top_35m_SD_mm', 'mean_top_35m_SD_mm', 'pseudo_align_35m_SD_mm', 'pseudo_align_70m_SD_mm', 'twist_3m_SD_mm', 'gps_fix_quality', 'gps_latitude_deg', 'gps_longitude_deg' ]
SWT_HEADER_ROW1 = 'DataReaderWriter, Version=1.2.700.0,Geometry,{0},,BBRL.UTGMS.CommonUtilities.DataTypes.FloatDataSampleSet'
SWT_HEADER_ROW2 = 'Time Stamp,Master Sync Inc,Master Sync State,Tacho,"AccelZ_Wb Invalid,AccelX_Wc Invalid,AccelX_Wd Invalid,AccelY_Wd Invalid,AccelY_Wp Invalid,Reserved Invalid,Right Dipped Joint Invalid,Left Dipped Joint Invalid,Left Top 35m Invalid,Right Top 35m Invalid,Mean Top 70m Invalid,Pseudo Align 35m Invalid,Pseudo Align 70m Invalid,Crosslevel Invalid,Twist 3m Invalid,Curvature Invalid,FQU|Fix Quality Invalid,LAS|Latitude Invalid,LOS|Longitude Invalid",Speed |MPH,AccelZ_Wb|m/s2,AccelX_Wc|m/s2,AccelX_Wd|m/s2,AccelY_Wd|m/s2,AccelY_Wp|m/s2,Reserved|N/A,Right Dipped Joint|mrads,Left Dipped Joint|mrads,Left Top 35m|mm,Right Top 35m|mm,Mean Top 70m|mm,Pseudo Align 35m|mm,Pseudo Align 70m|mm,Crosslevel|mm,Twist 3m|mm,Curvature|mm,Distance |km,Left Top 35m SD,Right Top 35m SD,Mean Top 70m SD,Pseudo Align 35m SD,Pseudo Align 70m SD,Twist 3m SD,FQU|Fix Quality,LAS|Latitude,LOS|Longitude'

# validate the rundate - must be yyyymmdd - and return a structured format
def valid_rundate(s):
	try:
		return datetime.strptime(s, '%Y%m%d')
	except ValueError:
		raise argparse.ArgumentTypeError("{0} is not a valid YYYYMMDD date".format(s))

# validate the dep time - must be HH:MM
def valid_deptime(s):
	try:
		return datetime.strptime(s, '%H:%M')
	except ValueError:
		raise argparse.ArgumentTypeError("{0} is not a valid HH:MM time".format(s))

		
def get_units(con, unit, trainid):
	'''
		Return a set of sqlite rows containing the UTGM units to create files for
		Params con = connection, unit = selected unit, trainid = selected train id
	'''
	logger.debug('gu {0} {1}'.format(unit, trainid))
	cursor_query = "SELECT DISTINCT unit FROM tt "

	if unit is None and trainid is None:
		cursor_query +=  ''
	else:
		cursor_query += 'WHERE '
		
	if trainid is not None:
		cursor_query  += 'trainid = :trainid '
		if unit is not None:
			cursor_query += 'AND unit = :unit'
	else:
		if unit is not None:
			cursor_query += 'unit = :unit'

	logger.debug('cq {0}'.format(cursor_query))
	return con.cursor().execute(cursor_query, {"unit": unit, "trainid": trainid})
	
		
def get_last_tacho(con, unit):
	'''
		Get the last tacho value for the selected unit
	'''
	cur_tacho = con.cursor().execute("SELECT last_tacho FROM tacho WHERE unit = :unit", {"unit": unit})
	return cur_tacho.fetchone()['last_tacho']


def get_geom_data(con, unit, rundate, trainid, dep_time, tacho, chunksize):
	'''
		Get geometry data for the specified date / unit / deptime.
		Return it as a pandas data table
	'''

	sql_query = (' '
	'SELECT tt.unit, tt.trainid, tt.fromloc, tt.deptime, geog.speedmpers as speed, '
	'datetime(julianday(:rundate||\' \'||tt.deptime) + geog.seconds/86400.0 + ((geom.offsetm-geog.offsetmstart)/geog.speedmpers)/86400.0) gpstimestamp, '			
	'printf(cast(round((julianday(:rundate||\' \'||tt.deptime) + geog.seconds / 86400.0 - julianday(\'0001-01-01\')) * 86400) as integer) * 10000000 + CASE  WHEN geog.speedmpers = 0 THEN 0 ELSE cast(((geom.offsetm-geog.offsetmstart)/geog.speedmpers * 10000000)   as integer)END) timestamp_ticks, '
	'geog.latitude as gps_latitude_deg, '
	'geog.longitude as gps_longitude_deg, '
	'geog.speedmpers, geom.offsetm, geog.metres, geog.seconds, ' #for checking
	':tacho + cast(30 * (geog.kminmetres + geom.offsetm) as int) tacho, '
	'COALESCE (overlay.left_top_35m_mm, geom.left_top_35m_mm ) as left_top_35m_mm, '
	'COALESCE (overlay.right_top_35m_mm, geom.right_top_35m_mm ) as right_top_35m_mm, '
	'COALESCE (overlay.mean_top_70m_mm, geom.mean_top_70m_mm ) as mean_top_70m_mm, '
	'COALESCE (overlay.pseudo_align_35m_mm, geom.pseudo_align_35m_mm ) as pseudo_align_35m_mm, '
	'COALESCE (overlay.pseudo_align_70m_mm, geom.pseudo_align_70m_mm ) as pseudo_align_70m_mm, '
	'COALESCE (overlay.crosslevel_mm, geom.crosslevel_mm ) as crosslevel_mm, '
	'COALESCE (overlay.twist_3m_mm, geom.twist_3m_mm ) as twist_3m_mm, '
	'COALESCE (overlay.curvature_mm, geom.curvature_mm ) as curvature_mm, '
	'COALESCE (overlay.right_dip_joint_mrad, geom.right_dip_joint_mrad ) as right_dip_joint_mrad, '
	'COALESCE (overlay.left_dip_joint_mrad, geom.left_dip_joint_mrad ) as left_dip_joint_mrad, '
	'7135416 master_sync_inc, '
	'\'FALSE\' master_sync_state, '
	'\'0000011111111110000\' flags, '			 
	'ROUND(geog.speedmpers*(3600/1609.3),3) as speed_mph, '
	'COALESCE (overlay.accel_z_wb_ms_2, geom.accel_z_wb_ms_2 ) as accel_z_wb_ms_2, '
	'COALESCE (overlay.accel_x_wc_ms_2, geom.accel_x_wc_ms_2 ) as accel_x_wc_ms_2, '
	'COALESCE (overlay.accel_x_wd_ms_2, geom.accel_x_wd_ms_2 ) as accel_x_wd_ms_2, '
	'COALESCE (overlay.accel_y_wd_ms_2, geom.accel_y_wd_ms_2 ) as accel_y_wd_ms_2, '
	'COALESCE (overlay.accel_y_wp_ms_2, geom.accel_y_wp_ms_2 ) as accel_y_wp_ms_2, '
	'0 reserved, '
	'ROUND((geog.kminmetres + geom.offsetm)/1000,4) as elapsed_distance_km, '			 
	'COALESCE (overlay.left_top_35m_SD_mm, geom.left_top_35m_SD_mm ) as left_top_35m_SD_mm, '
	'COALESCE (overlay.right_top_35m_SD_mm, geom.right_top_35m_SD_mm ) as right_top_35m_SD_mm, '
	'COALESCE (overlay.mean_top_35m_SD_mm, geom.mean_top_35m_SD_mm ) as mean_top_35m_SD_mm, '
	'COALESCE (overlay.pseudo_align_35m_SD_mm, geom.pseudo_align_35m_SD_mm ) as pseudo_align_35m_SD_mm, '
	'COALESCE (overlay.pseudo_align_70m_SD_mm, geom.pseudo_align_70m_SD_mm ) as pseudo_align_70m_SD_mm, '
	'COALESCE (overlay.twist_3m_SD_mm, geom.twist_3m_SD_mm ) as twist_3m_SD_mm, '
	'2 gps_fix_quality ' 
	'FROM tt '
	'INNER JOIN geog_train geog '
	'  ON geog.fromloc = tt.fromloc AND geog.toloc = tt.toloc '
	'INNER JOIN default_geom geom '
	'  ON geom.offsetm BETWEEN geog.offsetmstart AND geog.offsetmend '
	'LEFT OUTER JOIN geom_overlay overlay '
	'  ON overlay.startm = (geog.kminmetres + geom.offsetm) AND overlay.fromloc = geog.fromloc AND overlay.toloc = geog.toloc AND   :rundate BETWEEN overlay.fromdate and overlay.todate '
				 )
	# set up the where part of the query, dependent on what arguments are blank. Leave in geog seconds to keep it manageable
	sql_query += 'WHERE unit = :unit '

	if dep_time is not None:
		sql_query += 'AND unit = :unit AND tt.deptime = :dep_time '

	# add in optional filter for train id to WHERE statement 
	if trainid is not None:
		sql_query += 'AND trainid = :trainid '

	# debug
	if logger.getEffectiveLevel() == logging.DEBUG:
		sql_query += 'AND geog.seconds < {0} '.format(DEBUG_SECONDS)

	sql_query += 'ORDER BY tt.unit, tt.deptime, geog.seconds, geom.offsetm'
	logger.debug(sql_query)
	
	# chunked query because there are lots of rows 
	return sql.read_sql(sql_query, con, params={"rundate": rundate,"tacho": tacho, "dep_time": dep_time, "unit": unit, "trainid": trainid}, chunksize=chunksize )

	
def update_tacho(con, unit, tacho):
	'''
		update the tacho table with max tacho for unit
	'''
	con.cursor().execute('UPDATE tacho SET last_tacho = :last_tacho WHERE unit = :unit', {"last_tacho": tacho, "unit": unit })
	con.commit()
	

	
def create_csv(argvector):
	'''
	Creates .csv files of simulated Unattended Track Geometry Monitoring (UTGM) equipment output at the 0.2m grain.

	Creates one csv file for each UTGM unit implied by the provided command line arguments.

	Uses a sqlite database containing the source data tables.

	Accepts command line arguments for:
	 - sqlite database to use
	 - (optional) run date. If not specified, the current date is used
	 - (optional) unit id.  Identifier of a UTGM unit. If specified, will generate a file for this unit; if not specified,
	   will generate files for all the units represented in the database.
	 - (optional) departure time. If specified, will pick train(s) with this departure time; if not, will use all trains.
	 - (optional) train id. If specified, will pick just the specified train; otherwise all trains.
	 - (optional) debug. If specified, shows debug messages and a reduced set of data rows

	'''
	argparser = argparse.ArgumentParser(description='UTGM test data generator. Generates csv files of fake UTGM for a given date, UTGM unit and / or train departure time.', \
	epilog='(c) {0} Vivacity Rail Consulting Ltd for RSSB'.format(datetime.today().strftime('%Y')))
	argparser.add_argument('database', help='path to sqlite database to use')
	argparser.add_argument('--rundate', type=valid_rundate, help='Train run date in YYYYMMDD for today\'s date', default=datetime.today().strftime('%Y%m%d'))
	argparser.add_argument('--unit', help='UTGM unit (string) to run for. Leave blank for all units.')
	argparser.add_argument('--deptime', type=valid_deptime, help='train departure time string in HH:MM format. Leave blank for all trains for unit(s)/rundate')
	argparser.add_argument('--trainid', help='TrainID. Leave blank for all units.')
	argparser.add_argument('--debug', help='Debug flag - if specified, include debug messages and reduce query size', action='store_const', const=logging.DEBUG, default=logging.INFO)
	args = argparser.parse_args(argvector)

	unit = args.unit
	trainid = args.trainid
	dep_time = None
	if args.deptime is not None:
		dep_time = args.deptime.strftime('%H:%M:%S')
	rundate = args.rundate.strftime('%Y-%m-%d')
	logger.setLevel(args.debug)

	logger.info('Unit: {0} TrainID: {1} DepTime: {2} Run Date: {3}'.format(unit, trainid, dep_time, rundate))

	# connect to the database
	con = sqlite3.connect(args.database)
	con.row_factory = sqlite3.Row

	# generate a file for each unit implied by the run parameters, updating its tacho reading in the database
	for unitrow in get_units(con, unit, trainid):
		unit = unitrow['unit']
		logger.debug('ul: {0}'.format(unit))
		tacho = get_last_tacho(con, unit)

		# create empty temp file for output
		t = tempfile.NamedTemporaryFile(mode='w+t', delete=False)

		# write the headers to the file using the unit name
		t.write(SWT_HEADER_ROW1.format(unit) + '\n')
		t.write(SWT_HEADER_ROW2 + '\n')
		file_name = t.name
		t.close()

		rowcount = 0

		
		# get the table of data back in chunks and write to temp
		for geom_table in get_geom_data(con, unit, rundate, trainid, dep_time, tacho, CHUNKSIZE):
			geom_table['gps_ts_datetime'] = pd.to_datetime(geom_table['gpstimestamp'], utc=1, format='%Y-%m-%d %H:%M:%S')
			geom_table.to_csv(t, index=False, mode='a', header=False, columns=SWT_OUTPUT_COLUMNS)
			rowcount += geom_table.shape[0]
			logger.debug('ts: {0} rt: {1}'.format(geom_table.shape[0], rowcount))


	    # build the filename including gps time and rename temp file to it
		last_timestamp = geom_table['gps_ts_datetime'].max().strftime('%Y.%m.%d.%H%M%S') 
		outfilename = 'Geometry_{0}_{1}.csv'.format(unit, last_timestamp)
		shutil.copy(file_name, outfilename)
		os.remove(file_name)

		logger.info("{0} rows written to {1}".format(rowcount, outfilename)) 
		# update the tacho table with max tacho for unit
		update_tacho(con, unit, int(geom_table['tacho'].max()))

	return 0
		
if __name__ == "__main__":
	create_csv(sys.argv[1:])
	
	