#!/usr/bin/env python3

import requests
challenge_url = "http://localhost:8000"

response = requests.get(challenge_url)

token = response.json()["token"]

def multiply_list(num_list) :
    result = 1
    for num in num_list:
        result *= num
    return result

while "flag" not in response.json():
    objective = response.json()["objective"]
    numbers = response.json()["numbers"]

    answer = None

    if objective == "sum":
        answer = sum(numbers)
    elif objective == "multiply":
        answer = multiply_list(numbers)
    elif objective == "reverse":
        answer = list(reversed(numbers))
    elif objective == "sort": 
        answer = sorted(numbers)
    
    response = requests.post(challenge_url, json={"token": token, "answer": answer})

print("Solved! {}".format(response.json()["flag"]))
