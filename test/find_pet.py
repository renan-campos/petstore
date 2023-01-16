#
# Tests the Find behavior of the petstore web server.
#

import requests
import json

petstore_url = "http://localhost:8080"
pet_endpoint = "/api/v3/pet"
find_by_status_endpoint = "/api/v3/pet/findByStatus?status="

def create_payload(name, status=''):
    return json.dumps({'name': name, 'status': status})

def test(description, func):
    error = func()
    if error != "":
        return f"{description} failed: {error}"
    return ""

class Pet:
    def __init__(self, name, status):
        self.name = name
        self.status = status
    def create_payload(self):
        return create_payload(self.name, self.status)

def test_create_pets_with_status(pets):
    for pet in pets:
        try:
            response = requests.post(
                    url=f"{petstore_url}{pet_endpoint}",
                    data=pet.create_payload())
        except:
            return "Failed to connect to backend"
        if (response.status_code != 200):
            return "Expected 200 status code. Got: " + str(response.status_code)
        try:
            created_pet = response.json()
        except json.decoder.JSONDecodeError:
            return f"Failed to decode json {response}"
        if (created_pet['name'] != pet.name):
            return f"Expected pet name: {pet.name} got: {created_pet['name']}"
        if (created_pet['status'] != pet.status):
            return f"Expected pet status: {pet.status} got: {created_pet['status']}"
    return ""

def gen_create_pets_test(pets):
    return lambda: test_create_pets_with_status(pets)

def test_find_pets_with_status(pets, status):
    pets_with_status = [pet for pet in pets if pet.status == status]
    pet_names = [pet.name for pet in pets_with_status]
    for pet in pets:
        try:
            response = requests.get(
                    url=f"{petstore_url}{find_by_status_endpoint}{status}"
                    )
        except:
            return "Failed to connect to backend"
        if len(pets_with_status) == 0:
            if (response.status_code != 204):
                return f"Expected 204 status code. Got {response.status_code}"
        else:
            if (response.status_code != 200):
                return f"Expected 200 status code. Got {response.status_code}"
            try:
                returned_pets = response.json()
            except json.decoder.JSONDecodeError:
                return f"Failed to decode json {response}"
            if (len(returned_pets) != len(pet_names)):
                return f"The number of returned pets ({len(returned_pets)}) and expected pets ({len(pet_names)}) does not match"
            for returned_pet in returned_pets:
                if (not returned_pet['name'] in pet_names):
                    return f"Unexpected pet: {returned_pet['name']}"
        return ""


def gen_find_pets_with_status_test(pets, status):
    return lambda: test_find_pets_with_status(pets, status)

if __name__ == '__main__':
    pets = [
            Pet('Brady', 'pending'),
            Pet('Trickywoo', 'pending'),
            Pet('Marybell', 'pending'),
            Pet('Echo', 'sold'),
            ]
    tests = [
            test("Creating pets with status", gen_create_pets_test(pets)),
            test("Finding pets with status pending", gen_find_pets_with_status_test(pets, 'pending')),
            test("Finding pets with status sold", gen_find_pets_with_status_test(pets, 'sold')),
            test("Finding pets with invalid status", gen_find_pets_with_status_test(pets, 'foobar')),
            ]
    tests_passed = True
    for test_error in tests:
        if test_error != "":
            print(test_error)
            tests_passed = False
    if tests_passed: 
        print("All tests passed!")
