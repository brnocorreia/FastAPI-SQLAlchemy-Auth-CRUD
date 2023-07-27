import pytz
from sqlalchemy import Column, DateTime

from datetime import datetime

from core.configs import settings


class TimeStampedModel(settings.DBBaseModel):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


