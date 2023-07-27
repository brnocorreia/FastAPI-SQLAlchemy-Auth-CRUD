from typing import Optional

import datetime
from pydantic import BaseModel, HttpUrl


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    url_source: str
    user_id: Optional[int] = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
