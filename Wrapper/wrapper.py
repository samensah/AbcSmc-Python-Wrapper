#!/usr/local/bin/python3
import sqlite3
import json
import argparse

parser = argparse.ArgumentParser(description="Run AbcSmc")


def pjson(jsonfile):
	with open(jsonfile) as data_file:
		try:
			return json.load(data_file)
		except ValueError:
			print("invalid json input")
			exit()

def loadsim(myscript):
	exec (open(myscript).read())


parser.add_argument('myscript',
					type=loadsim, metavar='s',
					help='the .py or .pyc with your def simulate.'
)

parser.add_argument(
  'json',
  default="config.json", metavar="j",
  help="the .json with the parameters, metrics, and job data",
  type=pjson
)

parsed = parser.parse_args()

# connect python wrapper to Sqlite
conn = sqlite3.connect('/home/samuel/PycharmProjects/CAMS_Workshop/'
					   'AbcSmc_Python_Wrapper/Database/posterior.sqlite'
)


# parser.add_argument('iteration', type=int, default = 1)
# parser.add_argument('json_file', type=str, default = 'data.json')



def simulator() -> None:
  pass  # reading and writing to database

with conn:
	cur = conn.cursor()
	for row in cur.execute('SELECT * FROM parameters'):
		results = simulator(row)
		cur.execute('insert into metrics values (?,?,?,?,?,?,?,?)', results)