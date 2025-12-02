from fastapi import FastAPI, HTTPException, Body

app = FastAPI()
BOOKS = [
    {
        "title": "Book 1",
        "id": 1,
        "author": "a",
        "category": "xyz",
        "fav": True,
        "price": 15.75,
    },
    {
        "title": "Book 2",
        "id": 2,
        "author": "b",
        "category": "yzx",
        "fav": False,
        "price": 25.00,
    },
    {
        "title": "Book 3",
        "id": 3,
        "author": "c",
        "category": "zyx",
        "fav": False,
        "price": 17.50,
    },
    {
        "title": "Book 4",
        "id": 4,
        "author": "d",
        "category": "yxz",
        "fav": True,
        "price": 10.25,
    },
    {
        "title": "Book 5",
        "id": 5,
        "author": "e",
        "category": "xyz",
        "fav": False,
        "price": 5.99,
    },
]


@app.get("/books")
async def get_all_books():
    return {"message": "All Books", "length": len(BOOKS), "data": BOOKS}


@app.get("/books/fav")
async def get_fav_book():
    fav_books = [
        {k: v for k, v in book.items() if k != "fav"}
        for book in BOOKS
        if book.get("fav") == True
    ]
    return {
        "message": "All Books",
        "length": len(fav_books),
        "data": fav_books,
    }


@app.get("/books/id/{id}")
async def get_book_by_id(id: int) -> dict:
    book = next((b for b in BOOKS if b["id"] == int(id)), None)
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    book = {k: v for k, v in book.items() if k != "fav"}
    return {"message": f"Requested Book: {id}", "length": len(book), "data": book}


# @app.get("/books/")
"""
async def get_book_by_name(title: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("title").casefold() == title.casefold():
            books_to_return.append(book)

    if books_to_return:
        return {
            "message": f"Book found with title {title}",
            "length": len(books_to_return),
            "data": books_to_return,
        }
    raise HTTPException(status_code=404, detail="Book not found")
"""


@app.get("/books/author/{author}")
async def get_books_by_author_and_price(author: str, price: float = None) -> dict:
    books_to_return = BOOKS

    if author:
        books_to_return = [
            book
            for book in books_to_return
            if book.get("author").casefold() == author.casefold()
        ]

    if price is not None:
        books_to_return = [
            book for book in books_to_return if book.get("price") <= price
        ]

    if books_to_return:
        return {
            "message": "Books found",
            "length": len(books_to_return),
            "data": books_to_return,
        }
    raise HTTPException(status_code=404, detail="No books found")


@app.get("/books/")
async def get_book_by_query(
    title: str = None, author: str = None, category: str = None, price: float = None
):
    books_to_return = BOOKS

    if title:
        books_to_return = [
            book
            for book in books_to_return
            if book.get("title").casefold() == title.casefold()
        ]
    if author:
        books_to_return = [
            book
            for book in books_to_return
            if book.get("author").casefold() == author.casefold()
        ]
    if category:
        books_to_return = [
            book
            for book in books_to_return
            if book.get("category").casefold() == category.casefold()
        ]
    if price:
        books_to_return = [
            book for book in books_to_return if float(book.get("price")) <= float(price)
        ]
    if books_to_return:
        return {
            "message": f"Book found with title {title}",
            "length": len(books_to_return),
            "data": books_to_return,
        }
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/new_books")
async def add_new_book(new_book=Body(...)):
    new_book["id"] = len(BOOKS) + 1

    BOOKS.append(new_book)
    return {"message": f"{new_book['title']} Book added", "data": new_book}


@app.put("/books/update_book")
async def update_book(book: dict = Body(...)):
    updated_book = []
    if "id" in book:
        for i in range(len(BOOKS)):
            if BOOKS[i].get("id") == int(book["id"]):
                id = BOOKS[i].get("id")
                BOOKS[i] = book
                BOOKS[i]["id"] = id
                updated_book = BOOKS[i]
                break

    if not update_book and "title" in book:
        for i in range(len(BOOKS)):
            if BOOKS[i].get("title").casefold() == book["title"].casefold():
                id = BOOKS[i].get("id")
                BOOKS[i] = book
                BOOKS[i]["id"] = id
                updated_book = BOOKS[i]
                break

    if not updated_book:
        raise HTTPException(status_code=404, detail=f"Book not found")

    return {
        "message": f" {book['title']} Book updated",
        "length": 1,
        "data": updated_book,
    }


@app.delete("/books/delete/{param}")
async def delete_book(param) -> dict:
    deleted_book = []

    if param.isdigit():
        for book in range(len(BOOKS)):
            if BOOKS[book].get("id") == int(param):
                deleted_book = BOOKS.pop(book)
                break

    if not deleted_book:
        for book in range(len(BOOKS)):
            if BOOKS[book].get("title").casefold() == param.casefold():
                deleted_book = BOOKS.pop(book)
                break
    if not deleted_book:
        raise HTTPException(status_code=404, details="Book not found")

    return {"message": "Book Deleted", "length": 1, "data": deleted_book}
