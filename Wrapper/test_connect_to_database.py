import sqlite3
import json
import sys
#import 'myscript'

# connect python wrapper to Sqlite
conn = sqlite3.connect('/home/samuel/PycharmProjects/CAMS_Workshop/AbcSmc_Python_Wrapper/Database/Wrapper_database.sqlite')
print("Opened Wrapper_database database successfully")

#function to load .json data into wrapper
def load_jsondata(jsonfile):
	if jsonfile[-5:] == '.json':
		with open(jsonfile) as data_file:     
		    data = json.load(data_file)
		return data
	else:
		return 'Database must have a .json extension'

#def load_simulator(python_simulator):
#	if python_simulator[-3:] == '.py':
#		pass
#		#parse 'python_simulator.py' file into AbcSmc C++ function




jsondata = load_jsondata('data.json') #'data.json' will be replaced with sys.argv[5]
print(data)

#print examples
#print(data["maps"][0]["id"])
#print(data["masks"]["id"])
#print(data["om_points"])
