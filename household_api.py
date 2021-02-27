import os
import uuid
import json
import pickle
import ast
import csv
from flask_expects_json import expects_json
from jsonschema import ValidationError, SchemaError

from enum import Enum
from typing import List

import redis

from flask import (
    make_response,
    jsonify,
    request,
    Flask
)
from pydantic.main import BaseModel

app = Flask(__name__)

REDIS_HOST = os.environ.get('DB_HOST', 'localhost')


class Sex(str, Enum):
    male = 'male'
    female = 'female'


class User(BaseModel):
    age: int
    sex: Sex
    pregnancy:bool


class Household(BaseModel):
    members: List[User]
    income: float



## Schema for the HouseHold object
schema = {
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "age": { "type": "number", "minimum": 1 ,"maximum": 105  },
                "sex": { "enum": ["female", "male"] },
                "pregnancy": { "type": "boolean"}
            },
            "required": ["age", "sex"],
      		"additionalProperties" : False
        }
    },
    "type" : "object",
    "properties" : {
        "income" : {"type" : "number"},
        "members" : {
            "type": "array",
            "items" : {
                "$ref" : "#/definitions/User"
            },
         	"minItems": 1
        }
    }, "required": ["income", "members"],
       "additionalProperties" : False

}

## Returns redis connection object
def get_redis_connection():
    return redis.StrictRedis(host=REDIS_HOST)
    

## Handling errors with a response_code of 400
@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        return make_response(jsonify({'error': 'Invalid JSON schema'}), 400)
    elif isinstance(error.description, SchemaError):
        return make_response(jsonify({'error': 'Invalid JSON format'}), 400)
    return make_response(jsonify({'error': error.description}), 400)

## Handling an error with a response_code of 405
@app.errorhandler(405)
def bad_request(error):
    return make_response(jsonify({'error': 'Invalid URL'}), 405)



## POST request to store a Household object into redis database
## used @expects_json(schema) which performs schema validation and throws an error code of 400 if validation fails
## The method throws an error code of 500 if any internal error occurs
## The method returns a response code of 200 and id if it successfully stores the object
@app.route('/sample-household/', methods=['POST'])
@expects_json(schema)
def set_sample_household():
    try:
        id = uuid.uuid1().int 
        json_data = request.json
        obj = json.dumps(json_data)
    except Exception as e:
        status_code = 500
        return jsonify({'error': 'Internal error'}), status_code
    
    try: 
        r = get_redis_connection()
        r.set(id,  obj )
    except Exception as e: 
        status_code = 500
        return jsonify({'error': 'connection error'}), status_code
    
    status_code = 200
    return jsonify({'Id': id}), status_code




## GET request to get a Houldhold object from redis database
## The method requires id which it gets from path parameter named id
## If household is not present with an input id, the method returns an error code of 404
## For any database rleated error it throws an error code of 500
## It returns Household object with a status code of 200 if everything goes well
@app.route('/sample-household/<id>', methods=['GET'])
def get_sample_household(id):
    """
    Retrieves a static, sample household object

    This route exists to demonstrate the schema for a Household object.
    It does not touch Redis.
    """
    try:
        r = get_redis_connection()
        response_body= r.get(id)
        if(response_body==None):
            status_code = 404
            return jsonify({'error': 'No matching data'}), status_code
    except Exception as e: 
        status_code = 500
        return jsonify({'error': 'connection error'}), status_code
    
    status_code = 200
    
    return jsonify(json.loads(response_body.decode('utf-8'))), status_code
    # return jsonify(ast.literal_eval(response_body.decode('utf-8'))), status_code


## The method takes an input for id and state as path parameters and returns FPL percentage
## The method performs data scraping with pandas and Beautiful Soap, and stores table data into csv
## The method return 404 for missing data and 500 for internal server error
## It returns a status code of 200 with percentage if everything goes well
@app.route('/percentage-fpl/<id>/<state>', methods=['GET'])
def get_percentage_fpl(id, state):

    try:
        r = get_redis_connection()
        response_body= r.get(id)
    except Exception as e: 
        status_code = 500
        return jsonify({'error': 'connection error'}), status_code

    if(response_body==None):
        status_code = 404
        return jsonify({'error': 'No matching data'}), status_code

    try:
        json_data= json.loads(response_body)
        members = len(json_data['members'])
        income= float(json.dumps(json_data['income']))

        if state.lower() == "alaska":
            state="Alaska.csv"     
        elif state.lower() == "hawaii":
            state="Hawaii.csv"    
        else:
            state="Others.csv"
        with open(state, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if(members<=8): 
                for row in reader:
                    if(row['PERSONS IN FAMILY/HOUSEHOLD']==str(members)):
                        pay= int(row['POVERT GUIDLINES($)'])
                        percentage= income/pay
            else:
                for row in reader:
                    if(row['PERSONS IN FAMILY/HOUSEHOLD']=='8'):
                        pay= int(row['POVERT GUIDLINES($)'])
                if(state=="Alaska.csv"):
                    factor=5680
                elif(state=="Hawaii.csv"):
                    factor=5220
                else:
                    factor=4540       
                extra= members-8
                extra= extra*factor
                pay= pay + extra
                percentage= income/pay
    except Exception as e: 
        status_code = 500
        return jsonify({'error': 'Internal error'}), status_code


    status_code = 200
    return jsonify({'Percentage': round(percentage,4)}), status_code
    



@app.route('/eligibility/<id>', methods=['GET'])
def get_eligibility(id):
    try:
        r = get_redis_connection()
        response_body= r.get(id)
    except Exception as e: 
        status_code = 500
        return jsonify({'error': 'connection error'}), status_code

    if(response_body==None):
        status_code = 404
        return jsonify({'error': 'No matching data'}), status_code
    result= []
    try:
        json_data= json.loads(response_body)
        members = json_data['members']
        membercont= len(json_data['members'])
        
        with open('Others.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if(membercont<=8): 
                for row in reader:
                    if(row['PERSONS IN FAMILY/HOUSEHOLD']==str(membercont)):
                        pay= int(row['POVERT GUIDLINES($)'])
                        percentage= income/pay
            else:
                for row in reader:
                    if(row['PERSONS IN FAMILY/HOUSEHOLD']=='8'):
                        pay= int(row['POVERT GUIDLINES($)'])
                factor=4540       
                extra= membercont-8
                extra= extra*factor
                pay= pay + extra
                percentage= income/pay

        
        for member in members:
            age=member['age']
            preg=member['pregnancy']

            if age>=2 and age<=18 and percentage<=275:
                result.append(member)
            elif age<2 and age>0 and percentage<=283:
                result.append(member)
            elif preg == True and percentage<=278:
                result.append(member)
            elif percentage<=200:
                result.append(member)
    except Exception as e: 
        status_code = 500
        return jsonify({'error': 'Internal error'}), status_code

    status_code = 200
    return jsonify(result), status_code       

                


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
