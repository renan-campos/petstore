#
# A script to test uploading photos
# 
import hashlib
import json
import requests

petstore_url = "http://localhost:8080"
pet_endpoint = "/api/v3/pet"

def create_payload(name):
    return json.dumps({'name': name})

def create_pet(name):
    try:
        response = requests.post(
                url=petstore_url+pet_endpoint,
                data=create_payload(name)
                )
    except Exception as err:
        return f"Failed to connect to backend: {err}"
    if (response.status_code != 200):
        return f"Expected 200 status code. Got: {response.status_code}"
    created_pet = response.json()
    if (created_pet['name'] != name):
        return f"Expected pet name '{created_pet['name']} to equal '{pet_name}'"

def upload_pet_photo(pet_id, photo_fname):
    try:
        with open(photo_fname, 'rb') as f:
            response = requests.post(
                    url=f"{petstore_url}{pet_endpoint}/{pet_id}/uploadImage",
                    data=f
                    )
    except Exception as err:
        return f"Failed to connect to backend: {err}"
    if (response.status_code != 200):
        return f"Expected 200 status code. Got: {response.status_code}"
    photo_checksum = generate_checksum(photo_fname)
    if response.text != photo_checksum:
        return "Expected checksums to match:\n\t" + \
                f"{photo_checksum} (Expected)\n\t{response.text} (Received)"

def generate_checksum(fname):
    checksum = hashlib.sha256()
    with open(fname, 'rb') as f:
        checksum.update(f.read())
    return checksum.hexdigest()

if __name__ == '__main__':
    err = create_pet("Brady")
    if err != None:
        print(f"Failed to create pet: {err}")
        exit(1)

    err = upload_pet_photo(0, "dog.png")
    if err != None:
        print(f"Failed to upload photo: {err}")
        exit(1)

    print("Test passed!")
