from pydantic import BaseModel, Field, root_validator, validator
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    completed: bool

class TodoInDBBase(TodoBase):
    id: int
    created_at: datetime
    owner_id: int
    completed: bool 

    class Config:
        orm_mode = True

class Todo(TodoInDBBase):
    pass

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

    # Corrected validator for password
    @validator('password')
    def password_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Password must not be empty')
        return v 

class UserInDBBase(UserBase):
    id: int
    # Removed unique constraints in Pydantic models
    # Uniqueness is usually handled by the database schema, not Pydantic models
    
    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass
