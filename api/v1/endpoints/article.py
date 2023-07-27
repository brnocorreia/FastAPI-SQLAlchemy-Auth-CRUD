from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.article_model import ArticleModel
from models.user_model import UserModel
from schemas.article_schema import ArticleSchema
from core.deps import get_session, get_current_user

router = APIRouter()


# POST article
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArticleSchema)
async def post_article(
        article: ArticleSchema,
        logged_user: UserModel = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    new_article: ArticleModel = ArticleModel(
        title=article.title,
        description=article.description,
        url_source=article.url_source,
        user_id=logged_user.id
    )

    db.add(new_article)
    await db.commit()

    return new_article


# GET all articles
@router.get('/', response_model=List[ArticleSchema])
async def get_articles(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel)
        result = await session.execute(query)
        articles: List[ArticleModel] = result.scalars().unique().all()

        return articles


# GET one article
@router.get('/{article_id}', response_model=ArticleSchema, status_code=status.HTTP_200_OK)
async def get_article(article_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one_or_none()

        if article:
            return article

        raise HTTPException(detail=f'Article not found with id: {article_id}',
                            status_code=status.HTTP_404_NOT_FOUND)


# PUT one article
@router.put('/{article_id}', response_model=ArticleSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_article(article_id: int, article: ArticleSchema,
                         db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article_update: ArticleModel = result.scalars().unique().one_or_none()

        if article_update:
            if logged_user.id != article_update.user_id:
                raise HTTPException(detail='Users cannot modify articles they do not own.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)

            if article.title:
                article_update.title = article.title
            if article.description:
                article_update.description = article.description
            if article.url_source:
                article_update.url_source = article.url_source

            article_update.updated_at = datetime.utcnow()

            await session.commit()

            return article_update

        raise HTTPException(detail=f'Article not found with id: {article_id}',
                            status_code=status.HTTP_404_NOT_FOUND)


# DELETE one article
@router.delete('/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int,
                         db: AsyncSession = Depends(get_session),
                         logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article_delete: ArticleModel = result.scalars().unique().one_or_none()

        if article_delete:
            if logged_user.id != article_delete.user_id:
                raise HTTPException(detail='Users cannot delete articles they do not own.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)

            await session.delete(article_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(detail=f'Article not found with id: {article_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
