from typing import List, Optional, Any


from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaArticle, UserSchemaCreate, UserSchemaUpdate
from core.deps import get_session, get_current_user
from core.security import hash_generator
from core.auth import authenticate, create_access_token

router = APIRouter()


# GET Logged User
@router.get('/logged', response_model=UserSchemaBase)
def get_logged_user(logged_user: UserModel = Depends(get_current_user)):
    return logged_user


# POST / SignUp User
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=hash_generator(user.password),
        is_Admin=user.is_Admin
    )
    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(detail='Email already registered. Try login or create user with another one',
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)


# GET / All Users
@router.get('/', response_model=List[UserSchemaBase], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()

        return users


# GET / Unique User
@router.get('/{user_id}', response_model=UserSchemaArticle, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaArticle = result.scalars().unique().one_or_none()

        if user:
            return user

        raise HTTPException(detail=f'User not found with ID: {user_id}',
                            status_code=status.HTTP_404_NOT_FOUND)


# UPDATE / Unique User
@router.put('/{user_id}', response_model=UserSchemaArticle, status_code=status.HTTP_200_OK)
async def update_user_by_id(user_id: int,
                            user: UserSchemaUpdate,
                            db: AsyncSession = Depends(get_session),
                            logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_update: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_update:
            if logged_user.email != user_update.email:
                raise HTTPException(detail='Users cannot modify profiles they do not own.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)

            if user.name:
                user_update.name = user.name
            if user.surname:
                user_update.surname = user.surname
            if user.email:
                user_update.email = user.email
            if user.is_Admin:
                user_update.is_Admin = user.is_Admin
            if user.password:
                user_update.password = hash_generator(user.password)

            await session.commit()

            return user_update

        raise HTTPException(detail=f'User not found with ID: {user_id}',
                            status_code=status.HTTP_404_NOT_FOUND)


# DELETE / Unique User
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(user_id: int,
                         db: AsyncSession = Depends(get_session),
                         logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_delete: UserModel = result.scalars().unique().one_or_none()

        if user_delete:
            if logged_user.email != user_delete.email:
                raise HTTPException(detail='Users cannot delete profile they do not own.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)

            await session.delete(user_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(detail=f'User not found with id: {user_id}',
                            status_code=status.HTTP_404_NOT_FOUND)


# POST / Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect access data')

    return JSONResponse(content={"access_token": create_access_token(sub=user.id), "token_type": "bearer"},
                        status_code=status.HTTP_200_OK)
