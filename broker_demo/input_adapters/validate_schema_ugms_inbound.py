# schema validator. use this to validate the schema before using it

from tableschema import validate, exceptions
import sys

try:
	# validate the schema
	valid = validate('ugms_inbound_table_schema_swt_v0.01.json')
	print('OK')
	sys.exit(0)
except exceptions.ValidationError as exception:
	for error in exception.errors:
		print(error)
	sys.exit(1)


