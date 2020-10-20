import csv
import uuid
import os
from tableschema import Table, exceptions
from datetime import datetime, timedelta	
import json
import sys
import argparse
import time


# create_imprcm_format_ugms_csv_from_swt.py

# sample adapter to convert SWT-format files to broker-compliant csv format
# writes to an output file if specified, or to standard output for piping to a database
# optionally, validates the csv against the broker schema

# This shows how a T1010-01-compliant data provider can be created.
# Key points:
# - every referrable data item has a UUID
# - vendor-specific data can be embedded in the "extended items" sections as json
# - all measurement columns include unit of measure in title
# - the output file schema is well-defined using the Table Schema format
# - the output file in in .csv format so easily readable by downstream software and humans

# Created by Vivacity Rail Consulting Ltd for RSSB
# (c) 2019 RSSB

# headers that match the columns expected by the SWT flavour of the UGMS schema
HEADERS_OUT = ('file_timestamp_utc','file_name','file_uid','extended_items_metadata','timestamp_recorded_utc','extended_items_time','ugms_unit_id','ugms_unit_uid','gps_fix_quality','gps_latitude_deg','gps_longitude_deg','speed_as_recorded','speed_as_recorded_unit','elapsed_distance_as_recorded_m','extended_items_geography','left_top_35m_mm','right_top_35m_mm','crosslevel_mm','twist_3m_mm','left_top_35m_SD_mm','right_top_35m_SD_mm','mean_top_70m_SD_mm','twist_3m_SD_mm','left_dip_joint_mrad','right_dip_joint_mrad','pseudo_align_35m_mm','pseudo_align_70m_mm','pseudo_align_35m_SD_mm','pseudo_align_70m_SD_mm','mean_top_70m_mm','extended_items_geometry','accel_z_wb_ms_2','accel_x_wc_ms_2','accel_x_wd_ms_2','accel_y_wd_ms_2','accel_y_wp_ms_2','data_row_uid','creating_adapter_version')

# position of the SWT version identifier in the 1st header row
SWT_HEADER_VERSION_POS = 1

# SWT dodgy column names replaced with nicer ones
SWT_COLS = ('timestamp_ticks','master_sync_inc','master_sync_state','tacho','flags','speed_mph','accel_z_wb_ms_2','accel_x_wc_ms_2','accel_x_wd_ms_2','accel_y_wd_ms_2','accel_y_wp_ms_2','reserved','right_dip_joint_mrad','left_dip_joint_mrad','left_top_35m_mm','right_top_35m_mm','mean_top_70m_mm','pseudo_align_35m_mm','pseudo_align_70m_mm','crosslevel_mm','twist_3m_mm','curvature_mm','elapsed_distance_km','left_top_35m_SD','right_top_35m_SD','mean_top_35m_SD','pseudo_align_35m_SD','pseudo_align_35m_SD','twist_3m_SD','gps_fix_quality','gps_latitude_deg','gps_longitude_deg')

# details of this adapter
ADAPTER_VERSION = 'Vivacity-UGMS-Sample-v0.0.1'

# in the long run, the UGMS unit uuid will be provided by the supplier. Constant for now
UGMS_UNIT_UID = 'e4c27259-ed1c-4e6e-be7c-2b06966b0689'

# OUT_FILE_TEMPLATE = 'sample_output_file_IMPRCM_UGMS_inbound_SWT_{0}.csv'


def ticks_to_timestamp(ticks):
	# convert .net ticks to a timestamp
	return (datetime(1, 1, 1) + timedelta(microseconds = int(ticks)/10)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def gps_latlong_to_iso(lat, long):
	# convert lat and long to an ISO-6709 compliant pair
	return ''	



# parse the command line arguments
argparser = argparse.ArgumentParser(description='Converter SWT UGMS to IMPRCM csv', \
epilog='(c) {0} Vivacity Rail Consulting Ltd for RSSB'.format(datetime.today().strftime('%Y')))
argparser.add_argument('inputfile', type=argparse.FileType('r'), help='path to input .csv file of SWT format UGMS data')
argparser.add_argument('--schema', type=argparse.FileType('r'), help='path to json Table Schema file defining the schema to validate against')
argparser.add_argument('--outputfolder', help='output data folder path')
args = argparser.parse_args()

# get useful details out of the input filename
input_filename = os.path.basename(args.inputfile.name)
input_filename_elements = input_filename.split('_')
ugms_unit = input_filename_elements[1]
file_timestamp = datetime.strptime('.'.join(input_filename_elements[2].split('.')[:-1]), '%Y.%m.%d.%H%M%S').strftime('%Y-%m-%dT%H%M%SZ') # reformat to YYYY-HH-MMhhmmssZ

# get a uuid for the input file
# (note - this should be a property of the file itself, ideally part of the filename or listed in the header)
file_uuid = uuid.uuid4()

# construct the output file name
# print(args.outputfolder)
out_file = open(os.path.join(args.outputfolder, '_'.join([str(file_uuid), input_filename])), 'w')
# print(out_file.name)



# open the input file
with args.inputfile as fr:

	# pick the SWT file writer version from the first line of header
	swt_version = fr.readline().split(',')[SWT_HEADER_VERSION_POS].split('=')[1]

	# skip 2nd line of header - not used
	fr.readline()

	# open the output file
	with out_file as fw:

		wr = csv.DictWriter(fw, fieldnames=HEADERS_OUT, quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
		wr.writeheader()

		# read the rest of the file
		rr = csv.DictReader(fr, SWT_COLS)
		for input_row in rr:

			# map the columns from the input row
			output_row = {}
			output_row['file_timestamp_utc'] = file_timestamp
			output_row['file_name'] = input_filename
			output_row['file_uid'] = file_uuid

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
			output_row['gps_latitude_deg'] = round(float(input_row['gps_latitude_deg']),6)
			output_row['gps_longitude_deg'] = round(float(input_row['gps_longitude_deg']),6)
			output_row['speed_as_recorded'] = round(float(input_row['speed_mph']),3)
			output_row['speed_as_recorded_unit'] = 'mph'
			output_row['elapsed_distance_as_recorded_m'] = round(float(input_row['elapsed_distance_km']) * 1000,3)

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
			output_row['data_row_uid'] = uuid.uuid4()

			wr.writerow(output_row)

if args.schema is not None:
	# validate the output file against the schema
	# print(args.schema.name)
	tbl = Table(out_file.name, schema=args.schema.name)
	# print('checking...')
	try:
		tbl.read(limit=2000)
		print('OK')

	except exceptions.TableSchemaException as exception:
		for error in exception.errors:
			print(error)

time.sleep(5)