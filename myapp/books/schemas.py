from pydantic import BaseModel,Field
from typing import Annotated, Optional
from datetime import date
from uuid import UUID

# -------------------------
# Base Schema (shared)
# -------------------------
class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: Optional[date] = None
    page_count: Annotated[int, Field(ge=1)]
    language: str


# -------------------------
# Create Schema (POST)
# -------------------------
class BookCreate(BookBase):
    pass


# -------------------------
# Update Schema (PATCH)
# -------------------------
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[date] = None
    page_count: Optional[int] = Field(default=None, ge=1)
    language: Optional[str] = None



class BookResponse(BaseModel):
    id: UUID
    user_id : UUID
    title: str
    author: str
    publisher: str
    published_date: Optional[date]
    page_count: int
    language: str