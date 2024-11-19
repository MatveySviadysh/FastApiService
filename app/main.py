from fastapi import FastAPI
from routes.author_router import author_router

app = FastAPI()

app.include_router(author_router)