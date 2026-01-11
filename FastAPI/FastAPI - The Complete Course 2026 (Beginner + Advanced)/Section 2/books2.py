from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query, encoders
from pydantic import BaseModel, Field
from starlette import status
from datetime import date

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    publish_year: int
    description: str
    rating: int
    price: float

    def __init__(self, id, title, author, publish_year, description, rating, price):
        self.id = id
        self.title = title
        self.author = author
        self.publish_year = publish_year
        self.description = description
        self.rating = rating
        self.price = price


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Not needed in POST", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    publish_year: int = Field(gt=2000, lt=date.today().year)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    price: float = Field(gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Sample Book",
                "author": "Sample Author",
                "publish_year": 2000,
                "description": "Sample Description",
                "rating": 2,
            }
        }
    }


BOOKS = [
    Book(1, "Book 1", "Author 2", 1995, "A very nice book!", 5, 24.75),
    Book(2, "Book 2", "Author 4", 1985, "A great book!", 5, 30.30),
    Book(3, "Book 3", "Author 1", 1998, "A awesome book!", 5, 15.29),
    Book(4, "Book 4", "Author 1", 2020, "Book Description", 2, 22.99),
    Book(5, "Book 5", "Author 2", 2002, "Book Description", 3, 23.45),
    Book(6, "Book 6", "Author 3", 2025, "Book Description", 1, 25.00),
]


def book_id(book: Book):
    if len(BOOKS) > 1:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return {
        "message": "All Books",
        "length": len(BOOKS),
        "data": encoders.jsonable_encoder(BOOKS),
    }


@app.get("/books/rating", status_code=status.HTTP_200_OK)
async def get_book_by_rating(
    rating: int = Query(
        gt=0, lt=6, description="Provide the rating to filter greater or of same rating"
    )
):
    books_to_return = []
    for book in BOOKS:
        if book.rating >= rating:
            books_to_return.append(book)
    if books_to_return:
        return {
            "message": f"Found books with rating {rating} {"and above" if rating < 5 else ""}",
            "length": len(books_to_return),
            "data": encoders.jsonable_encoder(books_to_return),
        }
    raise HTTPException(status_code=404, detail=f"No book found with rating {rating}")


@app.get("/books/date", status_code=status.HTTP_200_OK)
async def get_books_by_publish_year(
    year: int = Query(
        gt=1900,
        lt=date.today().year,
        description="Provide the year to search for books in that year",
    )
) -> dict:
    match_books = []
    for book in BOOKS:
        if book.publish_year == int(year):
            match_books.append(book)

    if match_books:
        return {
            "message": "Found Book",
            "length": len(match_books),
            "data": encoders.jsonable_encoder(
                match_books
            ),  # converts the book python object to dict
        }
    raise HTTPException(status_code=404, detail=f"No book found in year {year}")


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(
    id: int = Path(gt=0, description="Enter the Book id to find the book")
) -> dict:
    for book in BOOKS:
        if book.id == int(id):
            return {
                "message": "Found Book",
                "length": 1,
                "data": encoders.jsonable_encoder(
                    book
                ),  # converts the book python object to dict
            }
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/update-books", status_code=status.HTTP_202_ACCEPTED)
async def update_book(book: BookRequest) -> dict:
    for i in range(len(BOOKS)):
        if book.id:
            if BOOKS[i].id == int(book.id):
                BOOKS[i] = book
                return {
                    "message": "Book details updated",
                    "length": 1,
                    "data": encoders.jsonable_encoder(BOOKS[i]),
                }
        if not book.id and book.title:
            if BOOKS[i].title == book.title:
                id = BOOKS[i].id
                BOOKS[i] = book
                BOOKS[i].id = id
                return {
                    "message": "Book details updated",
                    "length": 1,
                    "data": encoders.jsonable_encoder(BOOKS[i]),
                }

    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/add-book", status_code=status.HTTP_201_CREATED)
async def add_new_book(new_book: BookRequest):
    nb = Book(id=BOOKS[-1].id + 1, **new_book.model_dump())
    BOOKS.append(nb)
    # nb=Book(**new_book.model_dump())
    # BOOKS.append(book_id(nb))
    return {"message": "Added Book", "length": 1, "data": encoders.jsonable_encoder(nb)}


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(
    id: int = Path(gt=0, description="Provide the book id to delete book")
):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == int(id):
            BOOKS.pop(i)
            book_deleted = True
            break

    if not book_deleted:
        raise HTTPException(status_code=404, detail=f"No such book with id {id} found")
