#!/usr/local/bin/python3
import sqlite3
import json
import argparse
import subprocess as sub

def simulator(row):
	pass


parser = argparse.ArgumentParser(description="Run AbcSmc")


def pjson(jsonfile):
	with open(jsonfile) as data_file:
		try:
			return json.load(data_file)
		except ValueError:
			print("invalid json input")
			exit()

parser.add_argument('myscript',
					type=str, metavar='s',
					help='the .py or .pyc with your def simulate.'
)


parser.add_argument(
  'json',
  default="config.json", metavar="j",
  help="the .json with the parameters, metrics, and job data",
  type=pjson
)


parsed = parser.parse_args()


exec(open(parsed.myscript).read())


# connect python wrapper to Sqlite
conn = sqlite3.connect('/home/samuel/PycharmProjects/CAMS_Workshop/'
					   'AbcSmc_Python_Wrapper/Database/posterior.sqlite'
)


# parser.add_argument('iteration', type=int, default = 1)
# parser.add_argument('json_file', type=str, default = 'data.json')


with conn:
	cur = conn.cursor()
	for row in cur.execute('SELECT * FROM parameters'):
		results = simulator(row)
		cur.execute('insert into metrics values (?,?,?,?,?,?,?,?)', results)


# to read from command line
p = sub.Popen('date', stdout=sub.PIPE, stderr=sub.PIPE)
output, errors = p.communicate()
print(output)