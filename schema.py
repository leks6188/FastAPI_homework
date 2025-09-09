import uuid

from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class CreateAdvRequest(BaseModel):
    header: str
    description: str| None = None
    price: float
    owner: str

class CreateAdvResponse(BaseModel):
    id:int

class GetAdvResponse(BaseModel):
    header: str
    description: str
    price: float
    owner: str
    date_of_creation: datetime


class SearchAdvResponse(BaseModel):
    result: list[GetAdvResponse]

class UpdateAdvRequest(BaseModel):
    header: str|None=None
    description: str|None=None
    price: float|None=None
    owner: str|None=None

class UpdateAdvResponse(BaseModel):
    status:Literal["success"]

class DeleteAdvResponse(BaseModel):
    status:Literal["success"]

class LoginRequest(BaseModel):
    name:str
    password:str

class LoginResponse(BaseModel):
    token:uuid.UUID

class CreateUserRequest(BaseModel):
    name:str
    password:str
    role:str|None=None

class CreateUserResponse(BaseModel):
    id:int
    name:str

class UpdateUserRequest(BaseModel):
    name: str|None=None
    password:str|None=None

class DeleteUserResponse(BaseModel):
    status:Literal["success"]