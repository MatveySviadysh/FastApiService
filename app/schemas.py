import datetime
from typing import Optional
from pydantic import BaseModel

class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    photo: Optional[str] = None
    bio: Optional[str] = None
    birth_date: datetime.date
    death_date: Optional[datetime.date] = None

    class Config:
        orm_mode = True

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    photo: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[datetime.date] = None
    death_date: Optional[datetime.date] = None

class AuthorResponse(AuthorBase):
    id: int
    
    class Config:
        orm_mode = True
