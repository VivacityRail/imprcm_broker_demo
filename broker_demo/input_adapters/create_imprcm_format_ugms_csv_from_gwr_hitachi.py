import csv
import uuid
import os
from tableschema import Table, exceptions
from datetime import datetime, timedelta    
import json
import sys
import argparse


# create_imprcm_format_ugms_csv_from_gwr_hitachi.py

# sample adapter to convert class 800-format files to broker-compliant csv format
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

# headers that match the columns expected by the SWT flavour of the UGMS schema. Can copy from the range 'csv_header' in the schemas spreadsheet, tab "Inbound CSV"
HEADERS_OUT = ('file_timestamp_utc','file_name','file_uid','data_row_validity_flags','extended_items_metadata','timestamp_recorded_utc','extended_items_time','rail_unit_id','ugms_unit_id','ugms_unit_uid','extended_items_equipment','train_id','tacho_count','extended_items_travel','gps_fix_quality','gps_latitude_deg','gps_longitude_deg','gps_ground_speed_m_s','speed_as_recorded','speed_as_recorded_unit','elapsed_distance_as_recorded_m','gps_acquisition_mode','gps_altitude_m','gps_detail_of_satellites','gps_dgps_station_id','gps_ground_speed_km_h','gps_height_of_geoid_m','gps_hdop_m','gps_magnetic_track_made_good','gps_number_of_satellites','gps_pdop_m','gps_position_mode','gps_satellites_used','gps_seconds_since_last_dgps','gps_status','gps_true_track_made_good','gps_utc_time','gps_vdop','left_top_35m_mm','right_top_35m_mm','crosslevel_mm','twist_3m_mm','mean_alignment_35m_mm','gauge_mm','left_top_70m_mm','right_top_70m_mm','mean_top_70m_mm','mean_alignment_70m_mm','twist_5m_mm','gradient_deg','extended_items_geometry','aws_signal_strength_V','data_row_uid','creating_adapter_version')

# position of the Hitachi version identifier in the 1st header row
HITACHI_HEADER_VERSION_POS = 1

# Hitachi dodgy column names replaced with nicer ones. Can copy from the range 'python_header' in the schemas spreadsheet, tab "Inbound CSV"
HITACHI_COLS = ('x_timestamp_ticks','x_master_sync_inc','x_master_sync_state','tacho_count','x_data_status_flags','gps_acquisition_mode','gps_altitude_m','gps_detail_of_satellites','gps_dgps_station_id','gps_fix_quality','gps_ground_speed_km_h','gps_ground_speed_m_s','gps_height_of_geoid_m','gps_hdop_m','gps_latitude_deg','x_gps_latitude_direction','gps_longitude_deg','x_gps_longitude_direction','gps_magnetic_track_made_good','gps_number_of_satellites','gps_pdop_m','gps_position_mode','gps_satellites_used','gps_seconds_since_last_dgps','gps_status','gps_true_track_made_good','gps_utc_time','x_gps_date','x_gps_time','gps_vdop','x_master_imu_temp_c','x_master_camera_temp_c','x_master_imu_accel_long_ms_2','x_master_imu_accel_lat_ms_2','x_master_imu_acc_vert_ms_2','x_master_imu_rot_long_s_1','x_master_imu_rot_lat_s_1','x_master_imu_rot_vert_s_1','x_slave_imu_temp_c','x_slave_camera_temp_c','x_slave_imu_accel_long_ms_2','x_slave_imu_accel_lat_ms_2','x_slave_imu_acc_vert_ms_2','x_slave_imu_rot_long_s_1','x_slave_imu_rot_lat_s_1','x_slave_imu_rot_vert_s_1','left_top_35m_mm','right_top_35m_mm','left_top_70m_mm','right_top_70m_mm','mean_top_70m_mm','mean_alignment_35m_mm','mean_alignment_70m_mm','gauge_mm','crosslevel_mm','twist_3m_mm','twist_5m_mm','x_curvature_mm','gradient_deg','speed_as_recorded','aws_signal_strength_V','x_elapsed_distance_km','train_id','ugms_unit_id','x_driver_id','x_start_station_id','x_current_station_id','x_next_station_id','x_terminal_station_id')

# details of this adapter
ADAPTER_VERSION = 'Vivacity-UGMS-Inbound-Hitachi-v0.0.1'

# in the long run, the UGMS unit uuid will be provided by the supplier. Constant for now
UGMS_UNIT_UID = 'edeacd07-4c04-45c3-b0b5-39f6e0cc652f'

OUT_FILE_TEMPLATE = 'sample_output_file_IMPRCM_UGMS_inbound_Hitachi_{0}.csv'


def ticks_to_timestamp(ticks):
    # convert .net ticks to a timestamp
    return (datetime(1, 1, 1) + timedelta(microseconds = int(ticks)/10)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def gps_latlong_to_iso(lat, long):
    # convert lat and long to an ISO-6709 compliant pair
    return ''    



# parse the command line arguments
argparser = argparse.ArgumentParser(description='Converter SWT UGMS to IMPRCM csv', \
epilog='(c) {0} Vivacity Rail Consulting Ltd for RSSB'.format(datetime.today().strftime('%Y')))
argparser.add_argument('inputfile', type=argparse.FileType('r'), help='path to input .csv file of GWR Hitachi format UGMS data')
argparser.add_argument('--schema', type=argparse.FileType('r'), help='path to json Table Schema file defining the schema to validate against')
argparser.add_argument('--outputfile', help='output data file path - leave blank for std output')
args = argparser.parse_args()

# get useful details out of the input filename
# Hitachi filenames are of the form "Geometry_Euclid_Hitachi-WOE_T1_2018.12.20.191855.csv"
input_filename = os.path.basename(args.inputfile.name)
#print(input_filename)
input_filename_elements = input_filename.split('_')
ugms_unit = '-'.join(input_filename_elements[1:-1])
#print(ugms_unit)
file_timestamp = datetime.strptime('.'.join(input_filename_elements[-1].split('.')[:-1]), '%Y.%m.%d.%H%M%S').strftime('%Y-%m-%dT%H:%M:%SZ') # reformat to YYYY-HH-MMThh:mm:ssZ

# construct the output file name
if args.outputfile is None:
    out_file = sys.stdout
else:
    out_file = open(args.outputfile,'wb')

# get a uuid for the input file
# (note - this should be a property of the file itself, ideally part of the filename or listed in the header)
file_uuid = uuid.uuid4()

# open the input file
with args.inputfile as fr:

    # pick the Hitachi file writer version from the first line of header
    hitachi_version = fr.readline().split(',')[HITACHI_HEADER_VERSION_POS].split('=')[1]
    #print(hitachi_version)

    # skip 2nd line of header - not used
    fr.readline()


    #print(HEADERS_OUT)
    # open the output file
    with out_file as fw:

        wr = csv.DictWriter(fw, fieldnames=HEADERS_OUT, quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        wr.writeheader()

        # read the rest of the file
        rr = csv.DictReader(fr, HITACHI_COLS)
        for input_row in rr:
            #print(input_row)

            # map the columns from the input row
            output_row = {}
            output_row['file_timestamp_utc'] = file_timestamp
            output_row['file_name'] = input_filename
            output_row['file_uid'] = file_uuid

            # unvalidated extension point for non-standard metadata items
            output_row['extended_items_metadata'] = json.dumps({
                                                        'x_data_status_flags':  input_row['x_data_status_flags']
                                                        })

            output_row['timestamp_recorded_utc'] = ticks_to_timestamp(input_row['x_timestamp_ticks'])

            # unvalidated extension point for non-standard time items
            output_row['extended_items_time'] = json.dumps({
                                                        'x_timestamp_ticks':  input_row['x_timestamp_ticks'],
                                                        'x_master_sync_inc':  input_row['x_master_sync_inc'],
                                                        'x_master_sync_state':  input_row['x_master_sync_state']
                                                        })
            output_row['rail_unit_id'] = ''
            output_row['ugms_unit_id'] = ugms_unit
            output_row['ugms_unit_uid'] = UGMS_UNIT_UID

            output_row['extended_items_equipment'] = json.dumps({
                                                        'x_master_imu_temp_c':  input_row['x_master_imu_temp_c'],
                                                        'x_master_camera_temp_c':  input_row['x_master_camera_temp_c'],
                                                        'x_master_imu_accel_long_ms_2':  input_row['x_master_imu_accel_long_ms_2'],
                                                        'x_master_imu_accel_lat_ms_2':  input_row['x_master_imu_accel_lat_ms_2'],
                                                        'x_master_imu_acc_vert_ms_2':  input_row['x_master_imu_acc_vert_ms_2'],
                                                        'x_master_imu_rot_long_s_1':  input_row['x_master_imu_rot_long_s_1'],
                                                        'x_master_imu_rot_lat_s_1':  input_row['x_master_imu_rot_lat_s_1'],
                                                        'x_master_imu_rot_vert_s_1':  input_row['x_master_imu_rot_vert_s_1'],
                                                        'x_slave_imu_temp_c':  input_row['x_slave_imu_temp_c'],
                                                        'x_slave_camera_temp_c':  input_row['x_slave_camera_temp_c'],
                                                        'x_slave_imu_accel_long_ms_2':  input_row['x_slave_imu_accel_long_ms_2'],
                                                        'x_slave_imu_accel_lat_ms_2':  input_row['x_slave_imu_accel_lat_ms_2'],
                                                        'x_slave_imu_acc_vert_ms_2':  input_row['x_slave_imu_acc_vert_ms_2'],
                                                        'x_slave_imu_rot_long_s_1':  input_row['x_slave_imu_rot_long_s_1'],
                                                        'x_slave_imu_rot_lat_s_1':  input_row['x_slave_imu_rot_lat_s_1'],
                                                        'x_slave_imu_rot_vert_s_1':  input_row['x_slave_imu_rot_vert_s_1']
                                                        })
            output_row['train_id'] = input_row['train_id']
            output_row['tacho_count'] = input_row['tacho_count']
            output_row['extended_items_travel'] = json.dumps({
                                                        'x_driver_id':  input_row['x_driver_id'],
                                                        'x_start_station_id':  input_row['x_start_station_id'],
                                                        'x_current_station_id':  input_row['x_current_station_id'],
                                                        'x_next_station_id':  input_row['x_next_station_id'],
                                                        'x_terminal_station_id':  input_row['x_terminal_station_id']
                                                        })
            output_row['gps_fix_quality'] = input_row['gps_fix_quality']
            output_row['gps_latitude_deg'] = round(float(input_row['gps_latitude_deg']),6)
            output_row['gps_longitude_deg'] = round(float(input_row['gps_longitude_deg']),6)
            output_row['gps_ground_speed_m_s'] = input_row['gps_ground_speed_m_s']
            output_row['speed_as_recorded'] = round(float(input_row['speed_as_recorded']),3)
            output_row['speed_as_recorded_unit'] = 'mph'
            output_row['elapsed_distance_as_recorded_m'] = round(float(input_row['x_elapsed_distance_km']) * 1000,3)

            # unvalidated extension point for non-standard geography items
            #output_row['extended_items_geography'] = json.dumps({})

            output_row['gps_acquisition_mode'] = input_row['gps_acquisition_mode']
            output_row['gps_altitude_m'] = input_row['gps_altitude_m']
            output_row['gps_detail_of_satellites'] = input_row['gps_detail_of_satellites']
            output_row['gps_dgps_station_id'] = input_row['gps_dgps_station_id']
            output_row['gps_ground_speed_km_h'] = input_row['gps_ground_speed_km_h']
            output_row['gps_height_of_geoid_m'] = input_row['gps_height_of_geoid_m']
            output_row['gps_hdop_m'] = input_row['gps_hdop_m']
            output_row['gps_magnetic_track_made_good'] = input_row['gps_magnetic_track_made_good']
            output_row['gps_number_of_satellites'] = input_row['gps_number_of_satellites']
            output_row['gps_pdop_m'] = input_row['gps_pdop_m']
            output_row['gps_position_mode'] = input_row['gps_position_mode']
            output_row['gps_satellites_used'] = input_row['gps_satellites_used']
            output_row['gps_seconds_since_last_dgps'] = input_row['gps_seconds_since_last_dgps']
            output_row['gps_status'] = input_row['gps_status']
            output_row['gps_true_track_made_good'] = input_row['gps_true_track_made_good']
            output_row['gps_utc_time'] = input_row['gps_utc_time']
            output_row['gps_vdop'] = input_row['gps_vdop']

            output_row['left_top_35m_mm'] = input_row['left_top_35m_mm']
            output_row['right_top_35m_mm'] = input_row['right_top_35m_mm']
            output_row['crosslevel_mm'] = input_row['crosslevel_mm']
            output_row['twist_3m_mm'] = input_row['twist_3m_mm']
            output_row['mean_alignment_35m_mm'] = input_row['mean_alignment_35m_mm']
            output_row['gauge_mm'] = input_row['gauge_mm']
            output_row['left_top_70m_mm'] = input_row['left_top_70m_mm']
            output_row['right_top_70m_mm'] = input_row['right_top_70m_mm']
            output_row['mean_top_70m_mm'] = input_row['mean_top_70m_mm']
            output_row['mean_alignment_70m_mm'] = input_row['mean_alignment_70m_mm']
            output_row['twist_5m_mm'] = input_row['twist_5m_mm']
            output_row['gradient_deg'] = input_row['gradient_deg']

            # unvalidated extension point for non-standard geometry items
            output_row['extended_items_geometry'] = json.dumps({'curvature_mm': input_row['x_curvature_mm']})

            output_row['aws_signal_strength_V'] = input_row['aws_signal_strength_V']

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

