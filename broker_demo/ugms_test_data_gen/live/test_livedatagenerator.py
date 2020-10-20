import sys
#import sqlite3
import pandas as pd
# import pandas.io.sql as sql
import argparse
import logging
from datetime import datetime 
import os.path

'''
    Live test data generator
	Usage in python:
	>>>from test_livedatagenerator import emit_live_data
	>>>emit_live_data(['inputfile.cav'])

    or whatever you need the parameters to be	

'''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# refactor - move argument parser to a function
def arg_parser(argvector):
	argparser = argparse.ArgumentParser(description='UTGM live test data generator. Emits pseudo-live UTGM data lines from specified file', \
	epilog='(c) {0} Vivacity Rail Consulting Ltd for RSSB'.format(datetime.today().strftime('%Y')))
	argparser.add_argument('inputfile', type=argparse.FileType('r'), help='path to input .csv file of UTGM data to use')
	argparser.add_argument('--outputfile', type=argparse.FileType('w'), default=sys.stdout, help='path to where you want to output the data') # PJ: added default value sys.stdout
	return(argparser.parse_args(argvector))

	
def emit_live_data(argvector):
	'''
	Emit lines of simulated Unattended Track Geometry Monitoring (UTGM) equipment output at the 0.2m grain, in pseudo-live mode
	Reading from a specified file

	Accepts command line arguments for:
	 - csv file of track data to use

	'''
	args = arg_parser(argvector)
	with args.inputfile as f:
		df = pd.read_csv(f)

	logger.debug('Input rows: {0} Max seconds: {1}'.format(df.shape[0], df['seconds'].max()))
	starttime = datetime.now()
	logger.info('Start time: {0}'.format(starttime))

	with args.outputfile as f_out:   
		# iterate over the dataframe by seconds into run (df['seconds'])
		for sec in range(0, df['seconds'].max()):
	#	for sec in range(0, 10):
			# filter the dataframe so it only contains rows for the current second
			df_sec = df[df['seconds']==sec]
			# print out these rows one by one, with timestamp. 
			for i in range(0, df_sec.shape[0]):
				f_out.write(df_sec.iloc[i:i+1,:].to_csv(index=False, header=False).rstrip() + ',' + datetime.now().isoformat(timespec='microseconds') + '\n') # PJ: changed print to f_out.write() and put newline on the end

			# per the bullet point, just print out the number of seconds and the number of rows of data in that second
			print ('Second: {0}; rows: {1}; time:{2}'.format(sec, df_sec.shape[0],datetime.now().isoformat()))

	endtime = datetime.now()
	logger.info('End time: {0}'.format(endtime))
	logger.info('Duration: {0}'.format(endtime - starttime))

	return {'rows': df.shape[0], 'max_seconds': df['seconds'].max()}

if __name__ == "__main__":     # PJ: removed unwanted code and reverted to original
	emit_live_data(sys.argv[1:])
	
