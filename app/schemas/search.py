from pydantic import BaseModel, Field
from typing import List, Optional


class SSearchFilter(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None

class SSearchAdd(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    content_type: str = Field(...)

class SSearchDocument(BaseModel):
    title: str
    content: str
    content_type: str
    id: Optional[str] = Field(None, alias="_id")
    score: Optional[float] = Field(None, alias="_score")

    class Config:
        populate_by_name = True
