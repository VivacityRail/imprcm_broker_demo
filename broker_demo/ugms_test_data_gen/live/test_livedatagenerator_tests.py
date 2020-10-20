import unittest
from test_livedatagenerator import emit_live_data as emit_live_data
from test_livedatagenerator import arg_parser as arg_parser

# 6 add test for line count of file. Fails at this stage.
# 7 test now passes
# 8 fix test for missing file
# 9 add test of returned max_seconds in file

class TestEmitLiveDataFunction(unittest.TestCase):

	def test_call_with_no_arguments_fails(self):
		# test that if you call the program with no parameters, it exits with error
		self.assertRaises(SystemExit,arg_parser,[])	

	def test_call_with_nonexistent_file_fails(self):
		# test that if you call the program with a parameter which is not a real file, it exits with error
		self.assertRaises(SystemExit,arg_parser, ['inputfile.csv'])	

	def test_call_with_valid_file_returns_lines_and_seconds_in_file(self):
		# test that for a given data file, it returns the correct number of rows of data and max seconds
		return_dict = emit_live_data(['test_input.csv'])
		# print(return_dict)
		self.assertEqual(return_dict['rows'], 289996)	
		self.assertEqual(return_dict['max_seconds'], 1499)	

if __name__=="__main__":
   unittest.main()
