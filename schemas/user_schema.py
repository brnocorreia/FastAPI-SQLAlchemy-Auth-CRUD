from typing import Optional, List

from pydantic import BaseModel, EmailStr

from schemas.article_schema import ArticleSchema


class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    surname: str
    email: EmailStr
    is_Admin: bool = False

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaArticle(UserSchemaBase):
    articles: Optional[List[ArticleSchema]]


class UserSchemaUpdate(UserSchemaBase):
    name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_Admin: Optional[bool]









