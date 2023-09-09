from enum import Enum
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


class Directions(str, Enum):
    north = "North"
    east = "East"
    west = "West"
    south = "South"


BOOKS = {
    "book1": {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
    "book2": {"title": "1984", "author": "George Orwell"},
    "book3": {"title": "Pride and Prejudice", "author": "Jane Austen"},
    "book4": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    "book5": {"title": "One Hundred Years of Solitude", "author": "Gabriel García"},
    "book6": {"title": "Brave New World", "author": "Aldous Huxley"},
    "book7": {"title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    "book8": {"title": "Moby-Dick", "author": "Herman Melville"},
    "book9": {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
    "book10": {"title": "War and Peace", "author": "Leo Tolstoy"},
}


@app.get("/")
async def get_all_books():
    return BOOKS


@app.get("/books/{books_name}")
async def get_book_by_name(books_name: str):
    return BOOKS[books_name]


@app.get("/directions/{direction_name}")
async def get_directions(direction_name: Directions):
    if direction_name == Directions.north:
        return {"direction": "north", "sub": "up"}
    if direction_name == Directions.south:
        return {"direction": "south", "sub": "down"}
    if direction_name == Directions.east:
        return {"direction": "east", "sub": "left"}
    if direction_name == Directions.west:
        return {"direction": "west", "sub": "right"}


@app.get("/skip_book/")
async def skip_book(skip_book: Optional[str] = None):
    if skip_book:
        new_book = BOOKS.copy()
        del new_book[skip_book]
        return new_book
    else:
        return BOOKS


@app.post("/create_book")
async def create_book(book_title: str, book_author: str):
    count = 0

    if len(BOOKS) > 0:
        for _ in BOOKS:
            count += 1
    BOOKS[f"book_{count + 1}"] = {"title": book_title, "author": book_author}
    return BOOKS


@app.put("/update_book/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    BOOKS[book_name] = {"title": book_title, "author": book_author}
    return BOOKS


@app.delete("/delete_book/{book_name}")
async def delete_book(book_name: str):
    deleted_book = BOOKS[book_name]
    del BOOKS[book_name]
    return deleted_book


@app.delete("/delete_book/")
async def delete_book(book_name: str):
    deleted_book = BOOKS[book_name]
    del BOOKS[book_name]
    return deleted_book
