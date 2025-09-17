from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List

class UserProjects(BaseModel):
    name: str
    completed: bool

class UserLogs(BaseModel):
    date: date
    action: str

class UserTeam(BaseModel):
    name: str
    leader: bool
    projects: list[UserProjects]

class Users(BaseModel):
    id: str
    name: str 
    age: int
    score: int
    active: bool
    country: str
    team: UserTeam
    logs: List[UserLogs]

    model_config = ConfigDict(from_attributes=True)
    

