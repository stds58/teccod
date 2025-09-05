from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    content_type: Optional[str] = None  # например: "tutorial", "article" и т.п.

class SearchResponseItem(BaseModel):
    title: str
    snippet: str

class SearchResponse(BaseModel):
    results: List[SearchResponseItem]
