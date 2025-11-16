from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.questions import Question as QuestionModel
from app.models.answers import Answer as AnswerModel
from app.schemas import Answer as AnswerSchema, AnswerCreate

from app.db_depends import get_async_db

router = APIRouter(prefix='/answers', tags=['answers'])


@router.post('/{id}/answers', response_model=AnswerSchema, status_code=status.HTTP_201_CREATED)
async def create_answer(id: int, answer: AnswerCreate, db: AsyncSession = Depends(get_async_db)):
    temp = await db.scalars(select(QuestionModel).where(QuestionModel.id == id))
    question = temp.first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')
    new_answer = AnswerModel(question_id=id, user_id=answer.user_id, text=answer.text)
    db.add(new_answer)
    await db.commit()
    await db.refresh(new_answer)
    return new_answer

@router.get('/{id}', response_model=AnswerSchema, status_code=status.HTTP_200_OK)
async def get_all_answers(id: int, db: AsyncSession = Depends(get_async_db)):
    temp = await db.scalars(select(AnswerModel).where(AnswerModel.id == id))
    answer = temp.first()
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Answer not found')
    temp = await db.scalars(select(QuestionModel).where(QuestionModel.id == answer.question_id))
    question = temp.first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')
    return answer

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_answer(id: int, db: AsyncSession = Depends(get_async_db)) -> dict:
    temp = await db.scalars(select(AnswerModel).where(AnswerModel.id == id))
    answer = temp.first()
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Answer not found')

    await db.delete(answer)
    await db.commit()
    return {'message': 'Question deleted'}