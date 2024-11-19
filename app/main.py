from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime
from database.connect import SessionLocal, init_db
from database.models import Author

init_db()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    patronymic: str = None
    photo: str = None
    bio: str = None
    birth_date: datetime.date
    death_date: datetime.date = None

@app.post("/authors/", response_model=AuthorCreate)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
