# process incoming ugms data

import sys
import time
import psycopg2
import psycopg2.extras
import argparse



'''

    Process newly-arrived UGMS data files.  

    Scan the 'files_loaded' table for new files

    For each new file, fire off the processing pipeline

    Record the completion of the processing
 
'''

SLEEP_SECONDS = 10

SQL_LOAD_SANDCDATA = ('INSERT INTO public.ugms_s_and_c('
'    file_uid'
'    , extended_items_metadata'
'    , timestamp_recorded_utc'
'    , extended_items_time'
'    , ugms_unit_id'
'    , ugms_unit_uid'
'    , gps_fix_quality'
'    , gps_latitude_deg'
'    , gps_longitude_deg'
'    , speed_as_recorded'
'    , speed_as_recorded_unit'
'    , elapsed_distance_as_recorded_m'
'    , extended_items_geography'
'    , left_top_35m_mm'
'    , right_top_35m_mm'
'    , crosslevel_mm'
'    , twist_3m_mm'
'    , left_top_35m_sd_mm'
'    , right_top_35m_sd_mm'
'    , mean_top_70m_sd_mm'
'    , twist_3m_sd_mm'
'    , left_dip_joint_mrad'
'    , right_dip_joint_mrad'
'    , pseudo_align_35m_mm'
'    , pseudo_align_70m_mm'
'    , pseudo_align_35m_sd_mm'
'    , pseudo_align_70m_sd_mm'
'    , mean_top_70m_mm'
'    , extended_items_geometry'
'    , accel_z_wb_ms_2'
'    , accel_x_wc_ms_2'
'    , accel_x_wd_ms_2'
'    , accel_y_wd_ms_2'
'    , accel_y_wp_ms_2'
'    , data_row_uid'
'    , creating_adapter_version'
'    , unique_id'
'    , offset_along_s_and_c_m'
'    , direction_of_travel'
'    , main_elr'
'    , main_track_id'
'    , miles_decimal'
'    , miles_plus_yards'
')'
'    SELECT'
'    file_uid'
'    , extended_items_metadata'
'    , timestamp_recorded_utc'
'    , extended_items_time'
'    , ugms_unit_id'
'    , ugms_unit_uid'
'    , gps_fix_quality'
'    , gps_latitude_deg'
'    , gps_longitude_deg'
'    , speed_as_recorded'
'    , speed_as_recorded_unit'
'    , elapsed_distance_as_recorded_m'
'    , extended_items_geography'
'    , left_top_35m_mm'
'    , right_top_35m_mm'
'    , crosslevel_mm'
'    , twist_3m_mm'
'    , left_top_35m_sd_mm'
'    , right_top_35m_sd_mm'
'    , mean_top_70m_sd_mm'
'    , twist_3m_sd_mm'
'    , left_dip_joint_mrad'
'    , right_dip_joint_mrad'
'    , pseudo_align_35m_mm'
'    , pseudo_align_70m_mm'
'    , pseudo_align_35m_sd_mm'
'    , pseudo_align_70m_sd_mm'
'    , mean_top_70m_mm'
'    , extended_items_geometry'
'    , accel_z_wb_ms_2'
'    , accel_x_wc_ms_2'
'    , accel_x_wd_ms_2'
'    , accel_y_wd_ms_2'
'    , accel_y_wp_ms_2'
'    , data_row_uid'
'    , creating_adapter_version'
'    , unique_id'
'    , round(cast(u.elapsed_distance_as_recorded_m - s.main_forward_offset_start_m as numeric), 1) offset_along_s_and_c_m'
'    , t.direction direction_of_travel'
'    , s.main_elr'
'    , s.main_track_id'
'    , round(cast(u.elapsed_distance_as_recorded_m / 1609.3 as numeric), 6) miles_decimal'
'    , to_char(floor(u.elapsed_distance_as_recorded_m / 1609.3),\'000\') || \'+\' || to_char(round(cast((u.elapsed_distance_as_recorded_m / 1609.3 - floor(u.elapsed_distance_as_recorded_m / 1609.3)) * 1760 as numeric), 1),\'0000\')  miles_plus_yards'
' FROM ugms_touchdown u'
' INNER JOIN timetable_reference t'
' ON t.unit = u.ugms_unit_id'
' AND to_char(u.timestamp_recorded_utc, \'HH24MISS\') between to_char(t.deptime, \'HH24MISS\') and to_char(t.arrtime, \'HH24MISS\')'
' INNER JOIN s_and_c_reference s'
' ON ((u.elapsed_distance_as_recorded_m BETWEEN s.main_forward_offset_start_m - 40.0 AND s.main_forward_offset_end_m + 40.0 AND t.direction = 1)'
'  OR (u.elapsed_distance_as_recorded_m BETWEEN s.main_reverse_offset_start_m - 40.0 AND s.main_reverse_offset_end_m + 40.0 AND t.direction = -1))'
' WHERE file_uid = %s'
)


SQL_REFRESH_SANDC_SUMMARY = (
'INSERT INTO public.ugms_s_and_c_summary('
'    sample_date'
'    , left_top_35m_sd_mm'
'    , right_top_35m_sd_mm'
'    , mean_top_70m_sd_mm'
'    , twist_3m_sd_mm'
'    , pseudo_align_35m_sd_mm'
'    , pseudo_align_70m_sd_mm'
'    , unique_id'
'    , direction_of_travel'
'    , main_elr'
'    , main_track_id'
'    , miles_decimal_from'
'    , miles_plus_yards_from'
'    , miles_decimal_to'
'    , miles_plus_yards_to'
'    )'
'SELECT to_date(to_char(timestamp_recorded_utc, \'YYYYMMDD\'),\'YYYYMMDD\') as sample_date'
'    , avg(left_top_35m_sd_mm) left_top_35m_sd_mm'
'    , avg(right_top_35m_sd_mm) right_top_35m_sd_mm'
'    , avg(mean_top_70m_sd_mm) mean_top_70m_sd_mm'
'    , avg(twist_3m_sd_mm) twist_3m_sd_mm'
'    , avg(pseudo_align_35m_sd_mm) pseudo_align_35m_sd_mm'
'    , avg(pseudo_align_70m_sd_mm) pseudo_align_70m_sd_mm'
'    , u.unique_id'
'    , direction_of_travel'
'    , main_elr'
'    , main_track_id'
'    , min(miles_decimal) miles_decimal_from'
'    , to_char(floor(min(miles_decimal)), \'000\') || \'+\' || trim(to_char((min(miles_decimal) - floor(min(miles_decimal))) * 1760.0,\'0000\'))  miles_plus_yards_from'
'    , max(miles_decimal) miles_decimal_to'
'    , to_char(floor(max(miles_decimal)), \'000\') || \'+\' || trim(to_char((max(miles_decimal) - floor(max(miles_decimal))) * 1760.0,\'0000\'))  miles_plus_yards_to'
' FROM public.ugms_s_and_c u'
'  inner join files_loaded f'
' on f.file_uuid = u.file_uid'
' and f.processed_to_s_and_C_timestamp is not null                                                                                              '
' inner join wanted_s_and_cs w'
' on u.unique_id = w.unique_id'
' GROUP BY to_date(to_char(timestamp_recorded_utc, \'YYYYMMDD\'),\'YYYYMMDD\')'
'    , direction_of_travel'
'    , u.unique_id'
'    , main_elr'
'    , main_track_id'
)

def connect_to_db(connect_string):
    print('db connect: ', connect_string, flush=True)

    # wait for detabase to be ready, then connect
    while True:
        try:
            conn = psycopg2.connect(connect_string)
            break
        except psycopg2.OperationalError as oe:
            print("waiting for db...", flush=True)
            time.sleep(1)

    print('db status: ', conn.status, flush=True)
    return conn


def scan_for_new_files():

    # check for unprocessed files
    # print('scanning...', flush=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT file_name, file_uuid FROM files_loaded WHERE processed_to_s_and_c_timestamp IS NULL ORDER BY loaded_timestamp")
    next_file_to_do = cur.fetchone()
    if next_file_to_do:
        uuid_to_process = next_file_to_do['file_uuid']
        print('processing: ', next_file_to_do['file_name'], flush=True)
        # process the file (code from `load_wanted_sandc_geom_data.sql` in broker\Data Definition\Processing)
        sql = SQL_LOAD_SANDCDATA
        #print('uuid: ',  uuid_to_process, flush=True )
        cur.execute(sql, (uuid_to_process,))
        print('rows created: ', cur.rowcount, flush=True)
        conn.commit()

        cur.execute('DELETE FROM ugms_touchdown WHERE file_uid = %s', (uuid_to_process,))
        print('rows deleted: ', cur.rowcount, flush=True)
        conn.commit()
        cur.execute("UPDATE files_loaded SET processed_to_s_and_C_timestamp = current_timestamp WHERE file_uuid = %s", (uuid_to_process,))
        conn.commit()
        cur.close()

        # refresh the summary
        cur = conn.cursor()
        cur.execute("DELETE FROM ugms_s_and_c_summary")
        cur.execute(SQL_REFRESH_SANDC_SUMMARY)
        print('summary rebuilt', flush=True)
        cur.execute("UPDATE files_loaded SET summarised_timestamp = current_timestamp WHERE processed_to_s_and_c_timestamp IS NOT NULL and summarised_timestamp IS NULL")
        conn.commit()
        cur.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='UGMS data loader')
    parser.add_argument('--connection', type=str, default="host=localhost, port=5432")
    the_args = parser.parse_args()
    connect_string = the_args.connection

    conn = connect_to_db(connect_string)
    print('pipeline: listening for new data', flush=True)

    try:
        while True:
            scan_for_new_files()
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        sys.exit
