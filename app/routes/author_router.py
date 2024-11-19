from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import Author
from schemas import AuthorCreate, AuthorUpdate, AuthorResponse
from database.get_db import get_db

author_router = APIRouter()


@author_router.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """
    Создает нового автора и добавляет его в базу данных.
    
    - **author**: объект `AuthorCreate`, содержащий информацию о новом авторе.
    
    Если автор с такими же именем, фамилией и отчеством уже существует, 
    будет вызвано исключение с кодом 400.
    """
    existing_author = db.query(Author).filter(
        Author.first_name == author.first_name,
        Author.last_name == author.last_name,
        Author.patronymic == author.patronymic
    ).first()
    
    if existing_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@author_router.get("/authors/", response_model=List[AuthorResponse])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Получает список авторов из базы данных.
    
    - **skip**: количество авторов для пропуска (по умолчанию 0).
    - **limit**: максимальное количество авторов для возврата (по умолчанию 10).
    
    Возвращает список объектов `AuthorResponse`.
    """
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors


@author_router.get("/authors/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Получает автора по его ID.
    
    - **author_id**: ID автора, которого необходимо получить.
    
    Если автор с таким ID не найден, будет вызвано исключение с кодом 404.
    """
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@author_router.put("/authors/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    """
    Обновляет информацию о существующем авторе.
    
    - **author_id**: ID автора, которого необходимо обновить.
    - **author**: объект `AuthorUpdate` с новыми данными.
    
    Если автор с таким ID не найден, будет вызвано исключение с кодом 404.
    """
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    for key, value in author.dict().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author


@author_router.delete("/authors/{author_id}", response_model=dict)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """
    Удаляет автора по его ID.
    
    - **author_id**: ID автора, которого необходимо удалить.
    
    Если автор с таким ID не найден, будет вызвано исключение с кодом 404.
    Возвращает сообщение об успешном удалении.
    """
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(db_author)
    db.commit()
    return {"detail": "Author deleted successfully"}
