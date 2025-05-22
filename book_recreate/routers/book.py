# built-in libraries
from uuid import UUID
# installed libraries
from fastapi import APIRouter, HTTPException
# code libraries/folder
from database import books
from schemas.book import Response, BookCreate, BookUpdate
from services.book import book_service


book_router = APIRouter()


@book_router.get("")
def get_books():
    return books


@book_router.get("/{id}")
def get_book_by_id(id: str):
    book = book_service.get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found.")
    return book


@book_router.post("")
def add_book(book_in: BookCreate):
    book = book_service.create_book(book_in)
    return Response(message="Book added successfully", data=book)


@book_router.put("/{id}")
def update_book(id: str, book_in: BookUpdate):
    book = book_service.update_book(id, book_in)
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id: {id} not found"
        )
    return Response(message="Book updated successfully", data=book)


@book_router.delete("/{id}")
def delete_book(id: UUID):
    is_deleted = book_service.delete_book(id)
    if not is_deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id: {id} not found"
        )
    return Response(message="Book deleted successfully")
