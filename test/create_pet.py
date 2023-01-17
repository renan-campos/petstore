
#
# Tests the Get behavior of the petstore web server.
#

import requests
import json

petstore_url = "http://localhost:8080"
pet_endpoint = "/api/v3/pet"

def create_payload(name, status=''):
    return json.dumps({'name': name, 'status': status})

def test(description, func):
    error = func()
    if error != "":
        return f"{description} failed: {error}"
    return ""

def test_create_no_status():
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
        return f"Expected pet name '{created_pet['name']}' to equal {pet_name}"
    return ""

def test_create_valid_status():
    pet_name = 'Brady'
    pet_status = 'available'
    payload = create_payload(pet_name, pet_status)
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
        return f"Expected pet name '{created_pet['name']}' to equal {pet_name}"
    if (created_pet['status'] != pet_status):
        return f"Expected pet status '{created_pet['status']}' to equal {pet_status}"
    return ""

def test_create_invalid_status():
    pet_name = 'Brady'
    pet_status = 'foobar'
    payload = create_payload(pet_name, pet_status)
    try:
        response = requests.post(
                url=petstore_url+pet_endpoint,
                data=payload
                )
    except:
        return "Failed to connect to backend"
    if (response.status_code != 400):
        return f"Expected http status code '{str(response.status_code)}' to equal 400."
    violations = response.json()
    if (len(violations) != 1):
        return f"Expected one violation, got {len(violations)}"
    if ("not a valid status" not in violations[0]):
        return f"violation message does not talk about the status being invalid: '{violations[0]}'"
    if ("foobar" not in violations[0]):
        return f"Invalid status (foobar) not in violation message: '{violations[0]}'"
    return ""

if __name__ == '__main__':
    tests = [
            test("Creating a pet with no status specified", test_create_no_status),
            test("Creating a pet with a valid status specified", test_create_valid_status),
            test("Creating a pet with an invalid status", test_create_invalid_status),
            ]
    tests_passed = True
    for test_error in tests:
        if test_error != "":
            print(test_error)
            tests_passed = False
    if tests_passed: 
        print("All tests passed!")
