from typing import Union
from fastapi import FastAPI, HTTPException
import secrets
import datetime
import schemas
import random

app = FastAPI()

flag = "WMG{ScRipTInG_Is_VeRY_VeRY_UseFul_IsnT_It}"
successful_responses_required = 30
time_to_complete_challenge = 10

database = {}

def random_number_array(length = 10):
    return [random.randint(2,20) for i in range(length)]

def multiply_list(num_list) :
    result = 1
    for num in num_list:
        result *= num
    return result

def change_token_challenge(token: str):
    challenge = random.choice(["sum", "multiply", "reverse", "sort"])

    if challenge == "sum":
        random_numbers = random_number_array(40)
        instruction = "Sum the numbers!"
        database[token]["answer"] = sum(random_numbers)
    elif challenge == "multiply":
        random_numbers = random_number_array(10)
        instruction = "Multiply the numbers!"
        database[token]["answer"] = multiply_list(random_numbers)
    elif challenge == "reverse":
        random_numbers = random_number_array(30)
        instruction = "Reverse the list numbers!"
        database[token]["answer"] = list(reversed(random_numbers))
    elif challenge == "sort":
        random_numbers = random_number_array(20)
        instruction = "Sort the list of numbers in ascending order!"
        database[token]["answer"] = sorted(random_numbers)

    return challenge, instruction, random_numbers

@app.get("/", response_model=schemas.InitialChallenge)
def request_challenge():
    token = secrets.token_hex(16)
    database[token] = {
        "expires_at": datetime.datetime.now() + datetime.timedelta(seconds=time_to_complete_challenge),
        "successful_responses": 0
    }

    challenge, instruction, random_numbers = change_token_challenge(token)

    return {"instructions": "Hello there! You must send a POST request with the answer to the challenge below. If you answered it correctly, you will then receive another challenge. Repeat this over and over until you get the flag! Your POST request must be JSON, in the form {{'token': 'ABCDEF', 'answer': ...}} where the token is the token attached to this message. You have {} seconds to complete the challenge otherwise your token will expire. Your first challenge is:\n\n".format(time_to_complete_challenge) + instruction, "token": token, "objective": challenge, "numbers": random_numbers}

@app.post("/", response_model=Union[schemas.Challenge, schemas.Flag])
def submit_answer(request: schemas.ChallengeAnswer):
    if request.token not in database:
        raise HTTPException(410, detail="Your token is invalid, get a new one by sending a GET request!")
    
    db_entry = database[request.token]
    
    if db_entry["expires_at"] < datetime.datetime.now():
        del database[request.token]
        raise HTTPException(410, detail="This token has expired, get a new one by sending a GET request!")

    # Check whether they successfully did the challenge
    if request.answer != db_entry["answer"]:
        del database[request.token]
        raise HTTPException(410, detail="Incorrect answer - your token has now expired, get a new one by sending a GET request!")

    database[request.token]["successful_responses"] += 1

    # Check whether they've had enough successful responses to win
    if db_entry["successful_responses"] >= successful_responses_required:
        del database[request.token]
        return {
            "flag": flag
        }
    else:
        # Otherwise, give them another challenge
        challenge, instruction, random_numbers = change_token_challenge(request.token)

        return {"instructions": instruction, "objective": challenge, "numbers": random_numbers}
