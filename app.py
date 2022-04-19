# Python API with postgresSQL

import os
import json
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from psycopg2 import Error
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_query(selection=[]):
	connection = None # Set default value
	
	try:
		# In a real scenario you should hide credentials like these
		# using something like Docker Secrets or Hashicorp Vault

		uname = os.environ.get("user")
		db_pass = os.environ.get("pass")
		db_ip = os.environ.get("host")
		db_port = os.environ.get("port")
		db_name = os.environ.get("database")
		
		connection = psycopg2.connect(user=uname,
					password=db_pass,
					host=db_ip,
					port=db_port,
					database=db_name)
					
		# Create cursor to perform database operations
		cursor = connection.cursor()
		output = {}
		
		if not selection:
			# Executing a SQL query
			cursor.execute("SELECT * from works")
			
			# Fetch result
			record = cursor.fetchall()
			count = 1
			
			# Create dictionary from fetch results
			for row in record:
				output[count] = row[1], row[2], row[3], row[4]
				count += 1
			
			# return dictionary
			return json.dumps(output), 200, {'ContentType':'application/json'}
		else:
			for i in selection:
				# Verify i is a number
				if isinstance(i, int):
					# Executing a SQL query
					cursor.execute("SELECT title, authors, isbn, description FROM works WHERE work_id = %s", [i])
					
					# Fetch result
					record = cursor.fetchall()
					
					# Create dictionary from fetch results
					for row in record:
						output[i] = row[0], row[1], row[2], row[3]
				#else:
				#	print("Non integer input found!", i)
		
			return json.dumps(output), 200, {'ContentType':'application/json'}
		
		return json.dumps({'error': 'No valid input.'}), 200, {'ContentType':'application/json'}
	except(Exception, Error) as error:
		print("Error while connecting to server.", error)
		
		# Return error		
		return json.dumps({'error': 'Unable to connect or query server.'}), 500, {'ContentType':'application/json'}
	finally:
		if (connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed.")

@app.route('/selection', methods=['POST'])
def selection():
	# Check if input is a list
	if isinstance(request.get_json()['value'], list):
		subset = {}
		
		# verify list is not empty
		if request.get_json()['value']:
			subset = get_query(request.get_json()['value'])
			return subset
	
	# Return error
	return json.dumps({'error': 'Invalid input. Please set value to a list of numbers for work IDs.'}), 400, {'ContentType':'application/json'}

if __name__ == '__main__':
	app.run()

