from fastapi import FastAPI
from routers.book import book_router


app = FastAPI()

app.include_router(book_router, tags=["Books"], prefix="/books")


@app.get("/")
def home():
    return {"message": "Hello from the books API"}
