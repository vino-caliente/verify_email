from pydantic import BaseModel, EmailStr

class User(BaseModel):
    login: str
    email: EmailStr
    password: str

class ResendEmail(BaseModel):
    email: EmailStr