from uuid import UUID

from fastapi import FastAPI, Form, HTTPException, Request, status
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

app = FastAPI()


class NegativeNumberException(Exception):
    def __init__(self, books_to_return) -> None:
        super().__init__(books_to_return)


class BookWithoutRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: str = Field(
        min_length=1, max_length=100, title="Enter the Book description"
    )


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: str = Field(
        min_length=1, max_length=100, title="Enter the Book description"
    )
    rating: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "b607c581-d52d-44ba-b256-6c56f3fd9a6a",
                    "title": "Atomic Habits",
                    "author": "James Clear",
                    "description": "Its a self help Book",
                    "rating": 4,
                }
            ]
        }
    }


BOOKS = [
    Book(
        id="b607c581-d52d-44ba-b256-6c56f3fd9a6a",
        title="To Kill a Mockingbird",
        author="Harper Lee",
        description="Classic novel about racial injustice",
        rating=5,
    ),
    Book(
        id="b607c581-d52d-44ba-b256-6c58f3fd9a6a",
        title="1984",
        author="George Orwell",
        description="Dystopian future controlled by a totalitarian regime",
        rating=4,
    ),
    Book(
        id="b607c581-d82d-44ba-b256-6c56f3fd9a6a",
        title="Pride and Prejudice",
        author="Jane Austen",
        description="Classic romance novel",
        rating=4,
    ),
    Book(
        id="b607c581-d53d-44ba-b256-6c56f3fd9a6a",
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="Exploration of the American Dream in the 1920s",
        rating=4,
    ),
]


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(
    request: Request, exception: NegativeNumberException
):
    return JSONResponse(status_code=418, content="Negative numbers are not allowed")


# GET All books
@app.get("/books")
async def get_all_books():
    if len(BOOKS) < 1:
        return BOOKS
    return BOOKS


# GET Books by UUID
@app.get("/book/{book_id}")
async def get_books_by_id(book_id: UUID):
    for book in BOOKS:
        book.id == book_id
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/book/rating/{book_id}", response_model=BookWithoutRating)
async def get_books_by_id(book_id: UUID):
    for book in BOOKS:
        book.id == book_id
        return book
    raise HTTPException(status_code=404, detail="Book not found")


# POST Create New book
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return {"message": "Book created successfully"}


@app.post("/books/login")
async def book_login(username: str = Form(), passsword: str = Form()):
    return {"username": username, "passoord": passsword}


# PUT Update Book
@app.put("/update_book/{book_id}")
async def update_book(book_id: UUID, updated_book: Book):
    for i, existing_book in enumerate(BOOKS):
        if existing_book.id == book_id:
            BOOKS[i] = updated_book
            return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


# DELETE Delete Book by UUID
@app.delete("/delete_book/{book_id}")
async def delete_book(book_id: UUID):
    for i, existing_book in enumerate(BOOKS):
        if existing_book.id == book_id:
            del BOOKS[i]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
