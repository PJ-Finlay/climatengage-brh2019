import requests
import json

def info_for_location(address):
    params = {
            'key': 'AIzaSyAqooD1FdQHijP32vQk95Af5geX0gofCME',
            'address': address
        }

    response = requests.get('https://www.googleapis.com/civicinfo/v2/representatives', params=params)
    return json.loads(response.text)


