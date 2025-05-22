from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    id: str
    title: str
    author: str
    year: int
    pages: int
    language: str


class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    pages: int
    language: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    pages: Optional[int] = None
    language: Optional[str] = None


class Books(BaseModel):
    books: list[Book]


class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Book | Books] = None
