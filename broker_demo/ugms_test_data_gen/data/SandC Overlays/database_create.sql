/*
CREATE DATABASE imprcm_demo_raw
    WITH 
    OWNER = pete
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;
*/

DROP TABLE raw_ugms_swt;

CREATE TABLE raw_ugms_swt (
  unit varchar(40)
, file_timestamp varchar(255)
, timestamp_ticks bigint
, master_sync_inc integer
, master_sync_state boolean
, tacho integer
, flags varchar(19)
, speed_mph real
, accel_z_wb_ms_2 real
, accel_x_wc_ms_2 real
, accel_x_wd_ms_2 real
, accel_y_wd_ms_2 real
, accel_y_wp_ms_2 real
, reserved real
, right_dip_joint_mrad real
, left_dip_joint_mrad real
, left_top_35m_mm real
, right_top_35m_mm real
, mean_top_70m_mm real
, pseudo_align_35m_mm real
, pseudo_align_70m_mm real
, crosslevel_mm real
, twist_3m_mm real
, curvature_mm real
, elapsed_distance_km real
, left_top_35m_SD_mm real
, right_top_35m_SD_mm real
, mean_top_35m_SD_mm real
, pseudo_align_35m_SD_mm real
, pseudo_align_70m_SD_mm real
, twist_3m_SD_mm real
, gps_fix_quality real
, gps_latitude_deg real
, gps_longitude_deg real
);


create table processed_ugms_swt (
  unit varchar(40)
, file_timestamp varchar(255)
, file_datetime timestamp
, timestamp_ticks bigint
, timestamp_time timestamp
, master_sync_inc integer
, master_sync_state boolean
, tacho integer
, flags varchar(19)
, speed_mph real
, accel_z_wb_ms_2 real
, accel_x_wc_ms_2 real
, accel_x_wd_ms_2 real
, accel_y_wd_ms_2 real
, accel_y_wp_ms_2 real
, reserved real
, right_dip_joint_mrad real
, left_dip_joint_mrad real
, left_top_35m_mm real
, right_top_35m_mm real
, mean_top_70m_mm real
, pseudo_align_35m_mm real
, pseudo_align_70m_mm real
, crosslevel_mm real
, twist_3m_mm real
, curvature_mm real
, elapsed_distance_km real
, left_top_35m_SD_mm real
, right_top_35m_SD_mm real
, mean_top_35m_SD_mm real
, pseudo_align_35m_SD_mm real
, pseudo_align_70m_SD_mm real
, twist_3m_SD_mm real
, gps_fix_quality real
, gps_latitude_deg real
, gps_longitude_deg real
);

create table s_and_c_candidates (
ts_tix bigint);

