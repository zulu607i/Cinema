#!/usr/bin/python3

import requests
import json
import random
seat_seat = 'http://127.0.0.1:8000/api/seats/'
halls_url = 'http://127.0.0.1:8000/api/halls/'
payload = {}
headers = {'Authorization': 'Bearer MWZiYmM5YjE3MWEwNzM0MzlmMjQwYjI0ZDE5MjMzZDMxZDA3YzcyOA=='}

response_seats = requests.request("GET", seat_seat, headers=headers, data=payload)
response_halls = requests.request('GET', halls_url, headers=headers, data=payload)
halls = json.loads(response_halls.content)['results']
seats = json.loads(response_seats.content)['results']
random_nr_of_seats = random.randint(1, len(seats))

for i in seats[0:random_nr_of_seats]:
    if i['halls'] == halls[0]['id']:
        seat_id_url = f"http://127.0.0.1:8000/api/seats/{i['id']}/"
        if not i['is_occupied']:
            payload = {'is_occupied': True}
            requests.request("PUT", seat_id_url, headers=headers, data=payload)

        else:
            payload = {'is_occupied': False}
            requests.request("PUT", seat_id_url, headers=headers, data=payload)