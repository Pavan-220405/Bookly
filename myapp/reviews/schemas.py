from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID


class Review(BaseModel):
    book_id : Annotated[UUID,Field(...,description="ID of the book to review")]
    rating : Annotated[int,Field(...,description="Your rating for the book on a scale of 5",ge=1,le=5)]
    review_text : Annotated[str,Field(...,description="Your review about the book, strictly more than 20 characters",min_length=20)]


class ReviewCRUD(Review):
    user_id : Annotated[UUID,Field(...,description="ID of the user reviewing the book")]