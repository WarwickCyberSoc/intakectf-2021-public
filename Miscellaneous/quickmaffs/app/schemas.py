from typing import List, Union
from pydantic import BaseModel

class Challenge(BaseModel):
    instructions: str
    objective: str
    numbers: List[int]
    
class InitialChallenge(Challenge):
    token: str

class ChallengeAnswer(BaseModel):
    answer: Union[int, List[int]]
    token: str

class Flag(BaseModel):
    flag: str