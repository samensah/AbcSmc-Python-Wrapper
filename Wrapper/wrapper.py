#!/usr/bin/python
import sqlite3
import json
import argparse
import subprocess as sub
import os
import sys



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


parsed = parser.parse_args()

# check extension of simulator python script
def val_py(sim_file):
	return (os.path.splitext(sim_file)[1] == '.py') or (os.path.splitext(file)[1] == '.pyc')

# check extension of json file
def val_json(json_file):
	return os.path.splitext(json_file)[1] == '.json'

# check some specific key values in json
def checkjson(json_file):
	return 'smc_iterations' and 'num_samples' and \
	'database_filename' and 'parameters' and \
	'metrics' in json_file

# query to define the parameters
def build_select_query(json_data): #n is the serial_number
	par_names = []
	for par in json_data['parameters']:
		if 'short_name' in par:
			par_names.append('P.' + par['short_name'])
		else:
			par_names.append('P.' + par['name'])
	par_string = ', '.join(par_names)
	query = "select J.serial, P.seed, "
	query += par_string
	query += " from parameters P, jobs J where P.serial = J.serial "
    	query += "and (J.status = 'Q' or J.status = 'R') order by J.status, J.attempts;"
	return query

# query for metrics
def build_metrics_query(json_data, serial, met_values):
	met_values = map(str, met_values)
	met_names = []
	for met in json_data['metrics']:
		if 'short_name' in met:
			met_names.append(met['short_name'])
		else:
			met_names.append(met['name'])
	met_assignments = [met_names[i] + '=' + met_values[i] for i in range(len(met_names))]	
	met_string = ', '.join(met_assignments)
	#Check query 
	#only update metrics if job status is still 'R' or 'Q' or has been paused ('P')
	query = "update metrics set " + met_string + " where serial = " + str(serial) + " and (select (status is 'R' or status is 'Q' or status is 'P') from jobs where serial="+ str(serial) + ");"
	return query	


#build_metrics_query(parsed.json, 1, (1,2))
def build_update_jobs_query(serial):
	query =	"update jobs set status = 'D' where serial = " + str(serial) + " and (status = 'R' or status = 'Q' or status = 'P');"
	return query

def run_abc():
	p = sub.Popen(['./abc_sql', parsed.json, '--process'], stdout=sub.PIPE, stderr=sub.PIPE)
	output, errors = p.communicate()
	return output



# open and read simulator script
if val_py(parsed.myscript):
	exec(open(parsed.myscript).read())
else:
	print('The simulator script must be a .py or .pyc')

# open and load json data into memory
if val_json(parsed.json):
	with open(parsed.json) as data_file:
		json_data = json.load(data_file)
		if checkjson(json_data):
			pass
		else:
			sys.exit('Check documentation for json format')
else:
	print('The file must be a .json')

run_abc() # set up database


# connect python wrapper to Sqlite
conn = sqlite3.connect(json_data["database_filename"])

# for each smc set:
for iter_no in range(0, json_data["smc_iterations"] ):

	# for each particle:
	no_samples = json_data["num_samples"]
	for part in range(0, no_samples):
		select_query = build_select_query(json_data) #to call the parameters in the database
		with conn:
			cur = conn.cursor()
			cur.execute(select_query)
			par_values = cur.fetchone()[2:]
			print('par values', par_values)

		# run simulator
		sim_values = simulator(par_values)
		print('sim vlues:', sim_values)

		update_query = build_metrics_query(json_data, (no_samples*iter_no+part), sim_values) # to update the database
		

		#update metrics table
		cur.execute(update_query)
		

		#update jobs table
		cur.execute(build_update_jobs_query(part))
		
		conn.commit()
		#### capture and save output in a log file

	#out = run_abc()

		


	#run abc to start a new iteration
	p = sub.Popen(['./abc_sql', parsed.json, '--process'], stdout=sub.PIPE, stderr=sub.PIPE)  
	output, errors = p.communicate() 


	with open('output.txt', 'w') as textfile:
		textfile.write(output)

	

		





