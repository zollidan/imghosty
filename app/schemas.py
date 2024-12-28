from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, field_validator

class UserSchema(BaseModel):
    id: int 
    email: str
    first_name: str
    last_name: str
    password: str
    
class AddUserSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str

class UpdateUserSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str

