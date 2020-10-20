import csv
import uuid
from tableschema import Table, exceptions
from datetime import datetime

# sample adapter to create a minimal csv file that satisfies the XIRCM ugms input schema
#
# validates the csv against the broker schema
#
# minimal file must have the following columns:
#	file_timestamp_utc
#	file_name
#	timestamp_recorded_utc
#	ugms_unit_id
#	ugms_unit_uid
#	creating_adapter_version

SCHEMA = 'ugms_inbound_table_schema_minimal_v0.01.json'
OUT_FILE = 'test_minimal_xircm_ugms.csv'

ADAPTER_VERSION = 'Vivacity-UGMS-Sample-v0.0.1'
UGMS_UNIT_ID = 'ugms-00001'
UGMS_UNIT_UID = 'e4c27259-ed1c-4e6e-be7c-2b06966b0689'


# create a minimal csv file output
with open(OUT_FILE, 'w') as f:
	wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
	f.write('file_timestamp_utc,file_name,timestamp_recorded_utc,ugms_unit_id,creating_adapter_version\n')

	data_row = [
		'2019-02-18T07:45:23Z',
		OUT_FILE,
		datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
		UGMS_UNIT_ID,
		UGMS_UNIT_UID,
		ADAPTER_VERSION
	]
	wr.writerow(data_row)

# validate it against the schema
tbl = Table(OUT_FILE, schema=SCHEMA)
try:
	tbl.read()
	print('OK')
except exceptions.CastError as exception:
	for error in exception.errors:
		print(error)

except:
	pass