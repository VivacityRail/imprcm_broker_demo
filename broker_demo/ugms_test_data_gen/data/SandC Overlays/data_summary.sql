-- 1 row per second summary
select max(timestamp_ticks) tick, 
	avg(speed_mph) speed,
	sqrt(avg((case when abs(left_top_35m_mm) > 20 then 0 else left_top_35m_mm end)^2)) lt_rms,
	sqrt(avg((case when abs(right_top_35m_mm) > 20 then 0 else right_top_35m_mm end)^2)) rt_rms,
	sqrt(avg((case when abs(twist_3m_mm) > 20 then 0 else twist_3m_mm end)^2)) tw_rms,
	max(abs(case when abs(left_top_35m_mm) > 20 then 0 else left_top_35m_mm end)) lt_max,
	max(abs(case when abs(right_top_35m_mm) > 20 then 0 else right_top_35m_mm end)) rt_max,
	max(abs(case when abs(twist_3m_mm) > 20 then 0 else twist_3m_mm end)) tw_max,
	avg(gps_latitude_deg) lat,
	avg(gps_longitude_deg) long,
	count(*) points
from  raw_ugms_swt
group by left(timestamp_ticks::text, 11) 
order by left(timestamp_ticks::text, 11);
			
			
-- 1 row per 10m summary
select max(timestamp_ticks) tick, 
			avg(speed_mph) speed, 
			sqrt(avg((case when abs(left_top_35m_mm) > 20 then 0 else left_top_35m_mm end)^2)) lt_rms, 
			sqrt(avg((case when abs(right_top_35m_mm) > 20 then 0 else right_top_35m_mm end)^2)) rt_rms, 
			sqrt(avg((case when abs(twist_3m_mm) > 20 then 0 else twist_3m_mm end)^2)) tw_rms, 
			max(abs(case when abs(left_top_35m_mm) > 20 then 0 else left_top_35m_mm end)) lt_max, 
			max(abs(case when abs(right_top_35m_mm) > 20 then 0 else right_top_35m_mm end)) rt_max, 
			max(abs(case when abs(twist_3m_mm) > 20 then 0 else twist_3m_mm end)) tw_max, 
			avg(gps_latitude_deg) lat,
			avg(gps_longitude_deg) long, 
			count(*) points 
from raw_ugms_swt 
group by file_timestamp, (elapsed_distance_km * 100)::integer 
order by max(timestamp_ticks)				
					
					
select min(timestamp_ticks), min(file_Timestamp) from raw_ugms_swt;				-- "636516804716762765"
select max(timestamp_ticks), max(file_Timestamp) from raw_ugms_swt;				-- "636518662275060681"
					
					
-- get data nearby to candidate S&Cs - time of crossing +/- 20s either side
-- 20s is 200,000,000 ticks
					
select * from raw_ugms_swt u
inner join s_and_c_candidates s
on u.timestamp_ticks between s.ts_tix - 200000000 and ts_tix + 200000000	
order by ts_tix, timestamp_ticks					
					
					