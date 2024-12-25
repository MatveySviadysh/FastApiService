import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date

class AuthorBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    patronymic: Optional[str] = Field(None, min_length=2, max_length=100)
    photo: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    birth_date: date
    death_date: Optional[date] = None

    @validator('death_date')
    def validate_dates(cls, death_date, values):
        if death_date and values.get('birth_date'):
            if death_date < values['birth_date']:
                raise ValueError('Дата смерти не может быть раньше даты рождения')
        return death_date

    @validator('birth_date')
    def validate_birth_date(cls, birth_date):
        if birth_date > date.today():
            raise ValueError('Дата рождения не может быть в будущем')
        return birth_date

    class Config:
        orm_mode = True

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    patronymic: Optional[str] = Field(None, min_length=2, max_length=100)
    photo: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    birth_date: Optional[date] = None
    death_date: Optional[date] = None

    @validator('death_date')
    def validate_dates(cls, death_date, values):
        if death_date and values.get('birth_date'):
            if death_date < values['birth_date']:
                raise ValueError('Дата смерти не может быть раньше даты рождения')
        return death_date

class AuthorResponse(AuthorBase):
    id: int

    class Config:
        orm_mode = True
