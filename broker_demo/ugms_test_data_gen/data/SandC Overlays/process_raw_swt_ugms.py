import csv
import sys
import os
import argparse
from datetime import datetime

'''

 mangle a raw swt ugms file into the shape needed by postgres db
 This is basically the same, but has 2 items of file metadata at the start:
  - unit number
  - timestamp

'''
INPUT_FILE = 'D:\\GithubRepos\\IMPRCM\\broker\\Testing\\SampleData\\SWT\\Geometry_SWT-D-C159-012_2018.01.16.064140.csv'

# parse the input file argument
argparser = argparse.ArgumentParser(description='processor for raw SWT UGMS files - adds file metadata to each row', \
epilog='(c) {0} Vivacity Rail Consulting Ltd for RSSB'.format(datetime.today().strftime('%Y')))
argparser.add_argument('inputfile', type=argparse.FileType('r'), help='path to input .csv file of UGMS data to use')
argparser.add_argument('--outputfile', type=argparse.FileType('w'), default=sys.stdout, help='path to where you want to output the data') 
args = argparser.parse_args()

# get the unit number and file timestamp by parsing the filename, of form 'Geometry_SWT-D-C159-012_2018.01.16.064140.csv'
(unit, filestamp) = os.path.splitext(args.inputfile.name)[0].split('_')[-2:]

# read the file
with args.inputfile as ugms_file:
	# read top 2 lines of header and ignore them
	ugms_file.readline()
	ugms_file.readline()
	# write the file data out to stdout, putting the file metadata as the first two columns
	with args.outputfile as out_file:
		reader = csv.reader(ugms_file)
		for rows in reader:
			out_file.write(unit + ',' + filestamp + ',' + (','.join(map(str, rows))) + '\n')
