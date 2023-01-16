#
# Tests the Get behavior of the petstore web server.
#

import requests
import json

petstore_url = "http://localhost:8080"
pet_endpoint = "/api/v3/pet"

def create_payload(name):
    return json.dumps({'name': name})

def test(description, func):
    error = func()
    if error != "":
        return f"{description} failed: {error}"
    return ""

def test_create():
    pet_name = 'Brady'
    payload = create_payload(pet_name)
    try:
        response = requests.post(
                url=petstore_url+pet_endpoint,
                data=payload
                )
    except:
        return "Failed to connect to backend"
    if (response.status_code != 200):
        return "Expected 200 status code. Got: " + str(response.status_code)
    created_pet = response.json()
    if (created_pet['name'] != pet_name):
        return "Expected pet name: " + payload['name'] + "got: " + created_pet['name']
    return ""

def test_get():
    try:
        response = requests.get(
                url=f"{petstore_url}/{pet_endpoint}/0"
                )
    except:
        return "Failed to connect to backend"
    if (response.status_code != 200 ):
        return f"Expected 200 status code. Got: {response.status_code}"
    created_pet = response.json()
    if (created_pet['name'] != 'Brady'):
        return f"Expected pet name: 'Brady' got: {created_pet['name']}"
    return ""

def test_noget():
    try:
        response = requests.get(
                url=f"{petstore_url}/{pet_endpoint}/0"
                )
    except:
        return "Failed to connect to backend"
    if (response.status_code != 404):
        return f"Expected 404 status code. Got: {response.status_code}"
    return ""

if __name__ == '__main__':
    tests = [
            test("Getting a pet that doesn't exist", test_noget),
            test("Creating a pet", test_create),
            test("Getting a pet that does exist", test_get),
            ]
    tests_passed = True
    for test_error in tests:
        if test_error != "":
            print(test_error)
            tests_passed = False
    if tests_passed: 
        print("All tests passed!")
