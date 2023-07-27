import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from core.configs import settings
from models.base_model import TimeStampedModel


class ArticleModel(TimeStampedModel):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    description = Column(String(256))
    url_source = Column(String(256))
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("UserModel", back_populates='articles', lazy='joined')




