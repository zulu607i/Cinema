#!/usr/bin/python3
from urllib.parse import urljoin
import requests
import random

base_api_dns = 'http://127.0.0.1:8000/api/'
payload = {}
headers = {'Authorization': 'Bearer MWZiYmM5YjE3MWEwNzM0MzlmMjQwYjI0ZDE5MjMzZDMxZDA3YzcyOA=='}
response_halls = requests.get(urljoin(base_api_dns, 'halls/'),
                              headers=headers,
                              data=payload)
halls = random.choice(response_halls.json()['results'])
response_seats = requests.get(urljoin(base_api_dns, 'seats/'),
                              headers=headers,
                              data=payload,
                              params=f"halls__id={halls['id']}")

seats = response_seats.json()['results']
random_nr_of_seats = random.randint(1, len(seats))

for seat in seats[0:random_nr_of_seats]:
    if seat['halls'] == halls['id']:
        payload = {'is_occupied': not seat['is_occupied']}
        requests.put(urljoin(base_api_dns, f"seats/{seat['id']}/"), headers=headers, data=payload)
