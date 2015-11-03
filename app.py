from flask import Flask, request
from db import Connection
import json

app = Flask(__name__)
connection = Connection("localhost", "kool_plants", "postgres", "root")

def getLastInfo(plant_id, amount):
	query = "SELECT key, value FROM  periodic_values where plant_id = '{}'ORDER BY date DESC LIMIT {}".format(plant_id, amount)
	results = connection.execute(query)
	info = results
	result = []
	tmp = {}
	i = 0
	for row in info:
		i+=1
		tmp[row["key"]] = row["value"]
		if i % 4 == 0:
			result.append(tmp)
			tmp = {}
	return json.dumps(result, indent=2)

def getAllPlants():
	query = "SELECT * from plants"
	results = connection.execute(query)
	return json.dumps(results, indent=2)

def savePlant(body):
	query = "INSERT INTO plants (name) VALUES ('{}')".format(body["name"])
	result = connection.insert(query)

def saveInfo(body):
	id = body["id"]
	attributes = body["attributes"]
	for key, value in attributes.items():

		query = "INSERT INTO periodic_values (plant_id, key, value, date)VALUES ('{}', '{}', '{}', now())".format(id, key, value)
		result = connection.insert(query)

def postInstruction(body):
	command = body["command"]
	arguments = body["arguments"]
	query = "INSERT INTO instructions (command, arguments , status) VALUES ('{}', '{}', '{}')".format(command, arguments, 0)
	result = connection.insert(query)

def delInstruction(body):
	instruction_id = body["instruction_id"]
	query = "DELETE FROM instructions WHERE instruction_id = '{}'".format(instruction_id)
	result = connection.insert(query)
	return json.dumps(result, indent=2)

def getInstruction():
	query = "SELECT instruction_id, command, arguments from instructions where status = 0 order by instruction_id LIMIT 1"
	results = connection.execute(query)
	return json.dumps(results, indent=2)

@app.route("/receive", methods=["POST"])
def receive():
	
	json = request.get_json()
	saveInfo(json["plant"])
	return 'OK'

@app.route("/last/<plant_id>/<amount>", methods=["GET"])
def last(plant_id = None, amount = None):
	
	result = getLastInfo(plant_id, amount)
	return result

@app.route("/plants", methods=["POST"])
def plants():
	
	savePlant(request.get_json())
	return 'OK'

@app.route("/instructions", methods=["POST"])
def instructionPost():

	postInstruction(request.get_json())
	return 'OK'

@app.route("/instructions", methods=["GET"])
def instructionGet():

	return getInstruction()

@app.route("/instructions", methods=["DELETE"])
def instructionDel():

	return delInstruction(request.get_json())

@app.route("/plants", methods=["GET"])
def allPlants():
	result = getAllPlants()
	return result

if __name__ == "__main__":
	app.debug = True
	app.run(host= '0.0.0.0')
