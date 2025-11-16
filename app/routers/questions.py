from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.questions import Question as QuestionModel
from app.models.answers import Answer as AnswerModel
from app.schemas import Question as QuestionSchema, QuestionCreate

from app.db_depends import get_async_db

router = APIRouter(prefix='/questions', tags=['questions'])

@router.get('/', response_model=list[QuestionSchema], status_code=200)
async def get_all_questions(db: AsyncSession = Depends(get_async_db)):
    temp = await db.scalars(select(QuestionModel))
    questions = temp.all()
    return questions

@router.post('/', response_model=QuestionSchema, status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate, db: AsyncSession = Depends(get_async_db)):
    new_question = QuestionModel(**question.model_dump())
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_question_with_answer(id: int, db: AsyncSession = Depends(get_async_db)):
    temp = await db.scalars(select(QuestionModel).where(QuestionModel.id == id))
    question = temp.first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')

    temp = await db.scalars(select(AnswerModel).where(AnswerModel.question_id == id))
    answers = temp.all()
    return {'question': question, 'answers': answers}

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_question(id: int, db: AsyncSession = Depends(get_async_db)) -> dict:
    temp = await db.scalars(select(QuestionModel).where(QuestionModel.id == id))
    question = temp.first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')
    await db.delete(question)
    await db.commit()
    return {'message': 'Question deleted'}