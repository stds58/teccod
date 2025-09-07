from typing import Optional
from pydantic import BaseModel, Field


class SItemFilter(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None


class SItemDocument(BaseModel):
    title: str
    content: str
    content_type: str
    id: Optional[str] = Field(None, alias="_id")
    score: Optional[float] = Field(None, alias="_score")

    class Config:
        populate_by_name = True
