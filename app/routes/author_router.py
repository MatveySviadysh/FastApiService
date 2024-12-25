import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import Author
from schemas import AuthorCreate, AuthorUpdate, AuthorResponse
from database.get_db import get_db
import redis
author_router = APIRouter()

redis_client  = redis.Redis(host="localhost", port=6379, db=0)

@author_router.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """
    Создает нового автора и добавляет его в базу данных.
    Проверяет существование автора с такими же ФИО
    Если автор существует - возвращает ошибку 400
    Создает нового автора в базе данных
    Очищает связанный Redis-кэш
    Возвращает данные созданного автора
    """
    existing_author = db.query(Author).filter(
        Author.first_name == author.first_name,
        Author.last_name == author.last_name,
        Author.patronymic == author.patronymic
    ).first()
    
    if existing_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    db_author = Author(
        first_name=author.first_name,
        last_name=author.last_name,
        patronymic=author.patronymic
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    cache_keys = [f"author:{db_author.id}", "authors"]
    redis_client.delete(*cache_keys)
    return db_author


@author_router.get("/authors/", response_model=List[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    """
    Получает список всех авторов.
    Сначала проверяет наличие данных в Redis кэше.
    Если данные найдены в кэше - возвращает их.
    Если данных нет в кэше - получает список из базы данных,
    сохраняет в кэш на 10 минут и возвращает результат.
    Если авторов нет - возвращает HTTP 404.
    Возвращает список объектов `AuthorResponse`.
    """
    cache_key = "authors"
    check_authors = redis_client.get(cache_key)
    if check_authors:
        return json.loads(check_authors)
    authors = db.query(Author).all()
    if not authors:
        raise HTTPException(
            status_code=404,
            detail="Авторы не найдены"
        )
    
    authors_dict = [author.to_dict() for author in authors]
    redis_client.set(cache_key, json.dumps(authors_dict), ex=600)
    return authors


@author_router.get("/authors/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Получает информацию об авторе по его идентификатору.
    Сначала проверяет наличие данных в Redis кэше
    При отсутствии в кэше делает запрос к БД
    Кэширует полученные данные на 10 минут
    Если автор не найден, возвращает HTTP 404
    """
    cache_key = f"author:{author_id}"
    cached_author = redis_client.get(cache_key)
    if cached_author:
        return json.loads(cached_author)
    
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"Автор с идентификатором {author_id} не найден"
        )
    
    redis_client.set(cache_key, json.dumps(author.to_dict()), ex=600)
    return author


@author_router.put("/authors/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    """
    Обновляет информацию о существующем авторе в базе данных.
    Проверяет существование автора с указанным ID в базе данных
    Валидирует предоставленные данные для обновления
    Проверяет, не приведет ли обновление к дублированию ФИО с другим автором
    Обновляет данные автора в базе данных
    Очищает связанный кэш Redis
    """
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(
            status_code=404, 
            detail=f"Автор с идентификатором {author_id} не найден"
        )

    update_data = author.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Не предоставлены данные для обновления"
        )

    if any(field in update_data for field in ['first_name', 'last_name', 'patronymic']):
        existing_author = db.query(Author).filter(
            Author.id != author_id,
            Author.first_name == update_data.get('first_name', db_author.first_name),
            Author.last_name == update_data.get('last_name', db_author.last_name),
            Author.patronymic == update_data.get('patronymic', db_author.patronymic)
        ).first()
        if existing_author:
            raise HTTPException(
                status_code=400,
                detail="Автор с такими ФИО уже существует"
            )
    for key, value in update_data.items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    cache_keys = [f"author:{author_id}", "authors"]
    redis_client.delete(*cache_keys)
    return db_author


@author_router.delete("/authors/{author_id}", response_model=dict)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """
    Удаляет автора из базы данных и очищает связанный кэш.
    Проверяет существование автора в базе данных
    Удаляет автора из БД
    Очищает кэш для конкретного автора и общий список авторов
    """
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(
            status_code=404, 
            detail=f"Автор с идентификатором {author_id} не найден"
        )
    db.delete(db_author)
    db.commit()
    cache_keys = [f"author:{author_id}", "authors"]
    redis_client.delete(*cache_keys)
    return {"detail": "Автор успешно удален из системы"}
