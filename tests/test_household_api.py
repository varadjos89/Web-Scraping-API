import json
import requests

from mock import Mock

from redis import StrictRedis

from household_api import app
import pytest


# def test_get_household_returns_household():

#     redis_response = json.dumps({
#         "income": 100000.0,
#         "members": [
#             {
#                 "age": 105,
#                 "sex": "male"
#             },
#             {
#                 "age": 35,
#                 "sex": "male"
#             }
#         ]
#     })
#     mock_connection = Mock(spec_set=StrictRedis)
#     mock_connection.get.return_value = redis_response

#     with app.test_client() as client:
#         response = client.get('/sample_household/293426745440663156190935189158922878979')

#     assert response == redis_response


## The test case for POST request
## It's throwing an error 
@pytest.mark.xfail
def test_post_household_return_id():
    headers = {"Content-Type": "application/json"}
    payload=  {
        "income": 100000.0, 
        "members": [
            {
            "age": 105, 
            "sex": "male"
            }, 
            {
            "age": 35, 
            "sex": "male"
            }
        ]
    }
    url="http://localhost:8080/sample-household/"
    with app.test_client() as client:
        # response = requests.post(url, json=json.dumps(data))
        response = client.post(url, data=payload, headers=headers)
    assert response.status_code == 200


## The test case for GET request
@pytest.mark.parametrize("id",[('293426745440663156190935189158922878979')])
def test_get_data(id):
    url="http://localhost:8080/sample-household/"+id
    with app.test_client() as client:
        response= client.get(url)
    assert response.status_code == 200


## The test case for GET request
## The test case checks returned percentage
@pytest.mark.skip
@pytest.mark.parametrize("id, state, result",[('293426745440663156190935189158922878979','Alaska','4.5935')])
def test_get_percentile(id, state, result):
    url="http://localhost:8080/percentage-fpl/"+id+"/"+state
    with app.test_client() as client:
        response= client.get(url)
    assert response.status_code == 200
    assert response.Percentage == result