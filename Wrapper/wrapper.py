#!/usr/local/bin/python3
import sqlite3
import json
import argparse
import subprocess as sub
import os



def simulator(row):
	pass


parser = argparse.ArgumentParser(description="Run AbcSmc")

parser.add_argument('myscript',
					type=str, metavar='s',
					help='the .py or .pyc with your def simulate.')

parser.add_argument('json',
					default="config.json", metavar="j",
  					help="the .json with the parameters, metrics, and job data",
  					type=str)

# parser.add_argument('iteration',
# 					default="100", metavar="i",
# 					help="the number of iterations",
# 					type=int)
#
# parser.add_argument('sample_no', default="10", metavar="n",
# 					help="the number of samples",
# 					type=int)

parsed = parser.parse_args()

def val_py(file):
	filename, file_extension = os.path.splitext(file)
	return file_extension == '.py'


def val_json(file):
	filename, file_extension = os.path.splitext(file)
	return file_extension == '.json'


def checkjson(file):
	return 'smc_iterations' and 'num_samples' and \
	'database_filename' and 'parameters' and \
	'metrics' in file


if val_py(parsed.myscript):
	exec(open(parsed.myscript).read())
else:
	print('The simulator script must be a .py')


if val_json(parsed.json):
	with open(parsed.json) as data_file:
		data = json.load(data_file)
		if checkjson(data):
			pass
		else:
			print('Check documentation for json format')
else:
	print('The file must be a .json')



#check for the existence of a database, if exist check if is in the right format, the tables, if
#not create it
# connect python wrapper to Sqlite
conn = sqlite3.connect('/home/samuel/PycharmProjects/CAMS_Workshop/'
					   'AbcSmc_Python_Wrapper/Database/posterior.sqlite'
)


with conn:
	cur = conn.cursor()
	for row in cur.execute('SELECT * FROM parameters'):
		results = simulator(row)
		cur.execute('insert into metrics values (?,?,?,?,?,?,?,?)', results)


# to read from command line
p = sub.Popen('date', stdout=sub.PIPE, stderr=sub.PIPE)
output, errors = p.communicate()
#print(output)
