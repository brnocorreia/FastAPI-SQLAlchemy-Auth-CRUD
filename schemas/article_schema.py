from typing import Optional

import datetime
from pydantic import BaseModel, HttpUrl


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    url_source: str
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
