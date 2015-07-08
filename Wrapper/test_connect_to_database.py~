import sqlite3
import json
import sys
#import 'myscript'

# connect python wrapper to Sqlite
conn = sqlite3.connect('/home/samuel/PycharmProjects/CAMS_Workshop/AbcSmc_Python_Wrapper/Database/posterior.sqlite')
print("Opened Wrapper_database database successfully")


# read data from the parameter table in database into a list
with conn:
	mylist = []
	cur = conn.cursor()  
	for row in cur.execute('SELECT * FROM parameters'):
		mylist.append(list(row))
	print(mylist)

	#write data to metrics table in database
	for item in mylist:
		pass
		#results = myscript.simulator(row) #the rows are to be the input to the simulator function from the python script
		#cur.execute('insert into metrics values (?,?,?,?,?,?,?,?)', results)

	#test writing unto metrics table
	a = [1,2,3,4,5,6,7,8]
	cur.execute('insert into metrics values (?,?,?,?,?,?,?,?)', a)

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
print(jsondata)

#print examples
#print(data["maps"][0]["id"])
#print(data["masks"]["id"])
#print(data["om_points"])
