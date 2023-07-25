from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings


class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    is_Admin = Column(Boolean, default=False)
    articles = relationship(
        "ArticleModel",
        cascade="all, delete-orphan",
        back_populates="owner",
        uselist=True,
        lazy="joined"
    )




