#!/usr/local/bin/python3
import sqlite3
import json
import argparse

# connect python wrapper to Sqlite
conn = sqlite3.connect('/home/samuel/PycharmProjects/CAMS_Workshop/AbcSmc_Python_Wrapper/Database/posterior.sqlite')
print("Opened Wrapper_database database successfully")

parser = argparse.ArgumentParser(description="Run AbcSmc")
parser.add_argument('myscript', type=str, metavar = 'py_file')
# parser.add_argument('particles', type=int, default = 1)
# parser.add_argument('iteration', type=int, default = 1)
# parser.add_argument('json_file', type=str, default = 'data.json')

parsed = parser.parse_args()

def simulator() -> None:
    pass

# open user simulator python script and compile
exec(open(parsed.myscript).read())
print("Opened simulator python script successfully")


# reading and writing to database
with conn:
	cur = conn.cursor()
	for row in cur.execute('SELECT * FROM parameters'):
		results = simulator(row)
		cur.execute('insert into metrics values (?,?,?,?,?,?,?,?)', results)


#function to load .json data into wrapper
def load_jsondata(jsonfile):
	if jsonfile[-5:] == '.json':
		with open(jsonfile) as data_file:
			data = json.load(data_file)
		print("Opened and loaded json data into wrapper successfully")
		return data
	else:
		print('Database must have a .json extension')



