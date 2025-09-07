from typing import Optional
from pydantic import BaseModel, Field, computed_field


class SItemFilter(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None


class SItemDocument(BaseModel):
    title: str
    content: str = Field(exclude=True)

    @computed_field
    @property
    def snippet(self) -> str:
        return self.content[:50] + ("..." if len(self.content) > 50 else "")

    class Config:
        populate_by_name = True
