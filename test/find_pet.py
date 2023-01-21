#
# Tests the Find behavior of the petstore web server.
#

import requests
import json

petstore_url = "http://localhost:8080"
pet_endpoint = "/api/v3/pet"
find_by_status_endpoint = "/api/v3/pet/findByStatus?status="
find_by_tags_endpoint = "/api/v3/pet/findByTags?tags="

def create_payload(name, status='', tags=[]):
    return json.dumps({
                'name': name, 
                'status': status, 
                'tags': [{'name':tag} for tag in tags],
            })

def test(description, func):
    error = func()
    if error != "":
        return f"{description} failed: {error}"
    return ""

class Pet:
    def __init__(self, name, status='', tags=[]):
        self.name = name
        self.status = status
        self.tags = tags
    def create_payload(self):
        return create_payload(self.name, self.status, self.tags)

def test_create_pets_with_status_and_tags(pets):
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
        if (len(pet.tags) > 0 and len(created_pet['tags']) != len(pet.tags)):
            return f"Expected {created_pet['tags']} to equal {pet.tags}"
    return ""

def gen_create_pets_test(pets):
    return lambda: test_create_pets_with_status_and_tags(pets)

def test_find_pets_with_status(pets, statusList):
    pets_with_status = [pet for pet in pets if pet.status in statusList]
    pet_names = [pet.name for pet in pets_with_status]
    try:
        response = requests.get(
                url=f"{petstore_url}{find_by_status_endpoint}{','.join(statusList)}"
                )
    except Exception as err:
        return f"Failed to connect to backend: {err}"
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

def gen_find_pets_with_status_test(pets, statusList):
    return lambda: test_find_pets_with_status(pets, statusList)

def test_find_pets_with_tags(pets, tagList):
    pets_with_tags = pets
    for tag in tagList:
        pets_with_tags = [pet for pet in pets_with_tags if tag in pet.tags]
    pet_names = [pet.name for pet in pets_with_tags]
    try:
        response = requests.get(
                url=f"{petstore_url}{find_by_tags_endpoint}{','.join(tagList)}",
                )
    except Exception as err:
        return f"Failed to connect to backend: {err}"
    if len(pets_with_tags) == 0:
        if (response.status_code != 204):
            return f"Expected 204 status code. Got {response.status_code}"
        return ""
    if (response.status_code != 200):
        return f"Expected http status code {response.status_code} to equal 200"
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

def gen_find_pets_with_tags_test(pets, tagList):
    return lambda: test_find_pets_with_tags(pets, tagList)


if __name__ == '__main__':
    pets = [
            Pet('Brady', 'pending', ['afc-certified', 'backend_expert', 'good_boy']),
            Pet('Trickywoo', 'pending', ['afc-certified', 'backend_expert']),
            Pet('Marybell', 'pending', ['backend_expert']),
            Pet('Echo', 'sold', []),
            ]
    tests = [
            test("Creating pets with status and tags", gen_create_pets_test(pets)),
            test("Finding pets with status pending", gen_find_pets_with_status_test(pets, ['pending'])),
            test("finding pets with status sold", gen_find_pets_with_status_test(pets, ['sold'])),
            test("finding pets with either status sold or pending", gen_find_pets_with_status_test(pets, ['pending', 'sold'])),
            test("Finding pets with invalid status", gen_find_pets_with_status_test(pets, ['foobar'])),
            test("Finding pets with tag afc-certified", gen_find_pets_with_tags_test(pets, ['afc-certified'])),
            test("Finding pets with nonexistent tag", gen_find_pets_with_tags_test(pets, ['foobar'])),
            test("Finding pets with multiple tags", gen_find_pets_with_tags_test(pets, ['good_boy', 'backend_expert'])),
            test("Finding pets with multiple tags, and one is invalid", gen_find_pets_with_tags_test(pets, ['good_boy', 'foobar'])),
            ]
    tests_passed = True
    for test_error in tests:
        if test_error != "":
            print(test_error)
            tests_passed = False
    if tests_passed: 
        print("All tests passed!")
