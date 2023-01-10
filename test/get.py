#
# Tests the Get behavior of the petstore web server.
#

import requests
import json

petstore_url = "http://localhost:8080"
pet_endpoint = "/api/v3/pet"

def create_payload(name):
    return {'name': name}

def test(description, func):
    error = func()
    if error != "":
        return description + "failed: " + error
    return ""

def create_test():
    payload = create_payload('Brady')
    response = requests.post(
            url=petstore_url+pet_endpoint,
            data=json.dumps(
                create_payload('Brady')
                )
            )
    if (response.status_code != 200):
        return "Expected 200 status code. Got: " + str(response.status_code)
    created_pet = response.json()
    if (created_pet['name'] != payload['name']):
        return "Expected pet name: " + payload['name'] + "got: " + created_pet['name']
    return ""

if __name__ == '__main__':
    error = test("Creating a pet", create_test)
    if error != "":
        print(error)
    else:
        print("All tests passed!")
