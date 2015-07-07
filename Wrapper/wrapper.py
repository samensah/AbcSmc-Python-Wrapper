#!/usr/local/bin/python3
import sqlite3
import json
import argparse
import subprocess as sub


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

parser.add_argument('iteration',
					default="100", metavar="i",
					help="the number of iterations",
					type=int)

parser.add_argument('sample_no', default="10", metavar="n",
					help="the number of samples",
					type=int)

parsed = parser.parse_args()

exec(open(parsed.myscript).read())
with open(parsed.json) as data_file:
	try:
#check for the existence of various keys, check a num_samples keys and the datatype
		data = json.load(data_file)
	except ValueError:
		print("invalid json input")
		exit()







# data["num_samples"] = parsed.sample_no
# data["smc_iterations"] = parsed.iteration



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
