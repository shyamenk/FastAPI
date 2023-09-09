from enum import Enum

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
