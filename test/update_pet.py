#
# Tests the update behavior of the petstore web server.
#

import requests
import json

petstore_url = "http://localhost:8080"
pet_endpoint = "/api/v3/pet"

def test(description, func):
    error = func()
    if error != "":
        return f"{description} failed: {error}"
    return ""

def create_payload(name, status=''):
    return json.dumps({'name': name, 'status': status})

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

def test_update_name():
    pet_id = 0
    new_name = 'Brian'
    try:
        response = requests.post(
                url=f"{petstore_url}{pet_endpoint}/0?name={new_name}"
                )
    except Exception as err:
        return f"Failed to connect to backend: {err}"
    if (response.status_code != 200):
        return f"Expected 200 status code. Got: {response.status_code}"
    updated_pet = response.json()
    if (updated_pet['name'] != new_name):
        return f"Expected pet name '{updated_pet['name']}' to equal '{new_name}'"
    return ""

def test_update_status():
    pet_id = 0
    new_status = 'pending'
    try:
        response = requests.post(
                url=f"{petstore_url}{pet_endpoint}/0?status={new_status}"
                )
    except:
        return "Failed to connect to backend"
    if (response.status_code != 200):
        return f"Expected 200 status code. Got: {response.status_code}"
    updated_pet = response.json()
    if (updated_pet['status'] != new_status):
        return f"Expected pet status '{updated_pet['status']}' to equal '{new_status}'"
    return ""

def test_update_name_and_status():
    pet_id = 0
    new_name = 'Buddy'
    new_status = 'pending'
    try:
        response = requests.post(
                url=f"{petstore_url}{pet_endpoint}/0?name={new_name}&status={new_status}"
                )
    except Exception as err:
        return f"Failed to connect to backend: {err}"
    if (response.status_code != 200):
        return f"Expected 200 status code. Got: {response.status_code}"
    updated_pet = response.json()
    if (updated_pet['name'] != new_name):
        return f"Expected pet name '{updated_pet['name']}' to equal '{new_name}'"
    if (updated_pet['status'] != new_status):
        return f"Expected pet status '{updated_pet['status']}' to equal '{new_status}'"
    return ""

def test_invalid_update():
    pet_id = 0
    new_status = "foobar"
    try:
        response = requests.post(
                url=f"{petstore_url}{pet_endpoint}/0?status={new_status}"
                )
    except:
        return "Failed to connect to backend"
    if (response.status_code != 400):
        return f"Expected 400 status code. Got: {response.status_code}"
    violations = response.json()
    if len(violations) != 1:
        return f"Expected 1 violation. Got: {len(violations)}."
    if "not a valid status" not in violations[0]:
        return f"Expected violation to be about the invalid status. Got: {violations[0]}"
    return ""



if __name__ == '__main__':
    tests = [
            test("Creating a pet with status", test_create_valid_status),
            test("Updating pet name", test_update_name),
            test("Update pet status", test_update_status),
            test("Update both status and name", test_update_name_and_status),
            test("Invalid update", test_invalid_update),
            ]
    tests_passed = True
    for test_error in tests:
        if test_error != "":
            print(test_error)
            tests_passed = False
    if tests_passed: 
        print("All tests passed!")
