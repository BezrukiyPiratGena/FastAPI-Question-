# from app.database import Base, async_engine
#
# Base.metadata.create_all(bind=async_engine)

from fastapi import FastAPI
from app.routers import answers, questions

app = FastAPI(title='Тест задание', version='0.1.0')

app.include_router(questions.router)
app.include_router(answers.router)
