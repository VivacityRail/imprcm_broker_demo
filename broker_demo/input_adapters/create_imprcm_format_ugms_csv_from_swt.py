import csv
import uuid
import os
from tableschema import Table, exceptions
from datetime import datetime, timedelta	
import json

# sample adapter to convert SWT-format files to broker-compliant csv format

# validates the csv against the broker schema

# schema details
SCHEMA = 'ugms_inbound_table_schema_swt_v0.01.json'

# headers that match the columns expected by the SWT flavour of the schema
HEADERS_OUT = ('file_timestamp_utc','file_name','extended_items_metadata','timestamp_recorded_utc','extended_items_time','ugms_unit_id','ugms_unit_uid','gps_fix_quality','gps_latitude_deg','gps_longitude_deg','speed_as_recorded','speed_as_recorded_unit','elapsed_distance_as_recorded_m','extended_items_geography','left_top_35m_mm','right_top_35m_mm','crosslevel_mm','twist_3m_mm','left_top_35m_SD_mm','right_top_35m_SD_mm','mean_top_70m_SD_mm','twist_3m_SD_mm','left_dip_joint_mrad','right_dip_joint_mrad','pseudo_align_35m_mm','pseudo_align_70m_mm','pseudo_align_35m_SD_mm','pseudo_align_70m_SD_mm','mean_top_70m_mm','extended_items_geometry','accel_z_wb_ms_2','accel_x_wc_ms_2','accel_x_wd_ms_2','accel_y_wd_ms_2','accel_y_wp_ms_2','creating_adapter_version')

# position of the SWT version identifier in the 1st header row
SWT_HEADER_VERSION_POS = 1

# SWT dodgy column names replaced with nicer ones
SWT_COLS = ('timestamp_ticks','master_sync_inc','master_sync_state','tacho','flags','speed_mph','accel_z_wb_ms_2','accel_x_wc_ms_2','accel_x_wd_ms_2','accel_y_wd_ms_2','accel_y_wp_ms_2','reserved','right_dip_joint_mrad','left_dip_joint_mrad','left_top_35m_mm','right_top_35m_mm','mean_top_70m_mm','pseudo_align_35m_mm','pseudo_align_70m_mm','crosslevel_mm','twist_3m_mm','curvature_mm','elapsed_distance_km','left_top_35m_SD','right_top_35m_SD','mean_top_35m_SD','pseudo_align_35m_SD','pseudo_align_35m_SD','twist_3m_SD','gps_fix_quality','gps_latitude_deg','gps_longitude_deg')

# details of this adapter
ADAPTER_VERSION = 'Vivacity-UGMS-Sample-v0.0.1'

# in the long run, the UGMS unit uuid will be provided by the supplier. Constant for now
UGMS_UNIT_UID = 'e4c27259-ed1c-4e6e-be7c-2b06966b0689'

# INPUT_FILE = 'D:/Network Rail/UTGM Data/Input Data/DC159-012/Geometry_SWT-D-C159-012_2018.01.16.203152.csv'
INPUT_FILE = '../../../broker/Testing/SampleData/SWT/Geometry_SWT-D-C159-012_2018.01.16.064140.csv'
# INPUT_FILE = '../../../broker/Testing/SampleData/SWT/only2rowsGeometry_SWT-D-C159-012_2018.01.16.064140.csv'
OUT_FILE_TEMPLATE = 'sample_output_file_IMPRCM_UGMS_inbound_SWT_{0}.csv'


def ticks_to_timestamp(ticks):
	# convert .net ticks to a timestamp
	return (datetime(1, 1, 1) + timedelta(microseconds = int(ticks)/10)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def gps_latlong_to_iso(lat, long):
	return 0	

# get useful details out of the input filename
input_filename = os.path.basename(INPUT_FILE)
input_filename_elements = input_filename.split('_')
ugms_unit = input_filename_elements[1]
file_timestamp = datetime.strptime('.'.join(input_filename_elements[2].split('.')[:-1]), '%Y.%m.%d.%H%M%S').strftime('%Y-%m-%dT%H%M%SZ') # reformat to YYYY-HH-MMhhmmssZ

# construct the output file name
out_file = OUT_FILE_TEMPLATE.format(file_timestamp)

# open the input file
with open(INPUT_FILE, 'r') as fr:

	# pick the SWT file writer version from the first line of header
	swt_version = fr.readline().split(',')[SWT_HEADER_VERSION_POS].split('=')[1]

	# skip 2nd line of header with unfriendly column names
	fr.readline()

	# open the output file
	with open(out_file, 'w', newline='') as fw:

		wr = csv.DictWriter(fw, fieldnames=HEADERS_OUT, quoting=csv.QUOTE_MINIMAL)
		wr.writeheader()

		# read the rest of the file
		rr = csv.DictReader(fr, SWT_COLS)
		for input_row in rr:

			# map the columns from the input row
			output_row = {}
			output_row['file_timestamp_utc'] = file_timestamp
			output_row['file_name'] = input_filename

			# unvalidated extension point for non-standard metadata items
			output_row['extended_items_metadata'] = json.dumps({'flags': input_row['flags'],
																'reserved': input_row['reserved']})

			output_row['timestamp_recorded_utc'] = ticks_to_timestamp(input_row['timestamp_ticks'])

			# unvalidated extension point for non-standard time items
			output_row['extended_items_time'] = json.dumps({'timestamp_ticks': input_row['timestamp_ticks'], 
															'master_sync_state': input_row['master_sync_state'],
															'master_sync_inc' : input_row['master_sync_inc']})

			output_row['ugms_unit_id'] = ugms_unit
			output_row['ugms_unit_uid'] = UGMS_UNIT_UID
			output_row['gps_fix_quality'] = input_row['gps_fix_quality']
			# output_row['gps_position_iso'] = '' # not used as we are providing lat and long
			output_row['gps_latitude_deg'] = input_row['gps_latitude_deg']
			output_row['gps_longitude_deg'] = input_row['gps_longitude_deg']

			# unvalidated extension point for non-standard geography items
			output_row['extended_items_geography'] = json.dumps({})

			output_row['left_top_35m_mm'] = input_row['left_top_35m_mm']
			output_row['right_top_35m_mm'] = input_row['right_top_35m_mm']
			output_row['crosslevel_mm'] = input_row['crosslevel_mm']
			output_row['twist_3m_mm'] = input_row['twist_3m_mm']
			output_row['left_top_35m_SD_mm'] = input_row['left_top_35m_SD']
			output_row['right_top_35m_SD_mm'] = input_row['right_top_35m_SD']
			output_row['mean_top_70m_SD_mm'] = ''
			output_row['twist_3m_SD_mm'] = input_row['twist_3m_SD']
			output_row['left_dip_joint_mrad'] = input_row['left_dip_joint_mrad']
			output_row['right_dip_joint_mrad'] = input_row['right_dip_joint_mrad']
			output_row['pseudo_align_35m_mm'] = input_row['pseudo_align_35m_mm']
			output_row['pseudo_align_70m_mm'] = input_row['pseudo_align_70m_mm']
			output_row['pseudo_align_35m_SD_mm'] = input_row['pseudo_align_35m_SD']
			output_row['pseudo_align_70m_SD_mm'] = ''
			output_row['mean_top_70m_mm'] = input_row['mean_top_70m_mm']

			# unvalidated extension point for non-standard geometry items
			output_row['extended_items_geometry'] = json.dumps({'curvature_mm': input_row['curvature_mm']})

			output_row['accel_z_wb_ms_2'] = input_row['accel_z_wb_ms_2']
			output_row['accel_x_wc_ms_2'] = input_row['accel_x_wc_ms_2']
			output_row['accel_x_wd_ms_2'] = input_row['accel_x_wd_ms_2']
			output_row['accel_y_wd_ms_2'] = input_row['accel_y_wd_ms_2']
			output_row['accel_y_wp_ms_2'] = input_row['accel_y_wp_ms_2']
			output_row['creating_adapter_version'] = ADAPTER_VERSION

			wr.writerow(output_row)

# validate it against the schema
tbl = Table(out_file, schema=SCHEMA)
try:
	tbl.read()
	print('OK')

except exceptions.CastError as exception:
	for error in exception.errors:
		print(error)

except:
	pass

