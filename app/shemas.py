import datetime
from pydantic import BaseModel

class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    patronymic: str = None
    photo: str = None
    bio: str = None
    birth_date: datetime.date
    death_date: datetime.date = None

    class Config:
        orm_mode = True

class AuthorCreate(AuthorBase):
    pass
