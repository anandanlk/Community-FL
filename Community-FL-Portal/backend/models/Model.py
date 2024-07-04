from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    type: str
    group: str
    dataURL: Optional[str] = None
    modelURL: Optional[str] = None
    uid: Optional[str] = None
    tags: Optional[list[str]] = None
    status: Optional[str] = "Offline"
    reserved_by: Optional[str] = None
    weights: Optional[str] = None
    client_ip: Optional[str] = None
    last_seen: Optional[int] = 0

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Client(BaseModel):
    username: str
    client_ip: Optional[str] = None

class Reservation(BaseModel):
    no_of_clients: int
    duration: float
    username: Optional[str] = None
    status: Optional[str] = None