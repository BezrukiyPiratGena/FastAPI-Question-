from pydantic import BaseModel, Field
from datetime import datetime

class Question(BaseModel):
    id: int = Field(description='ID вопроса')
    text: str = Field(description='Текст вопроса')
    created_at: datetime = Field(description='Дата и время публикации вопроса')

class QuestionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=100, description='Текст вопроса')

class Answer(BaseModel):
    id: int = Field(description='ID Ответа')
    question_id: int = Field(description='ID родительского вопроса(Question)')
    user_id: str = Field(description='Идентификатор пользователя')
    text: str = Field(description='Текст ответа')
    created_at: datetime = Field(description='Дата и время публикации ответа')

class AnswerCreate(BaseModel):

    user_id: str = Field(min_length=36, max_length=36, description='Идентификатор пользователя')
    text: str = Field(min_length=1, max_length=500, description='Текст ответа')
