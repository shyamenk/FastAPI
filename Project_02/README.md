# PROJECT 2

---

### Pydantic Data Model

- `Base Model` - Used to create a Schema
- `Validation` - `Fields` from pydantic

---

### FAST API CRUD Operations

- `GET` - GET all the Books
- `GET` - Get books by UUID
- `PUT` - Update books by UUID
- `POST` - Create neww Books
- `DEL` - Delete a book by UUID

### Exception in FASt API

In FastAPI, you can raise exceptions to handle error cases in your API. One common way to handle exceptions is by using the HTTPException class, which allows you to return specific HTTP status codes along with a custom error message.

#### Raise HTTP Exception

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=400, detail="Item ID cannot be zero")
    return {"item_id": item_id}

```

#### Custom HTTP Exception

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

class CustomException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise CustomException("Item ID cannot be zero")
    return {"item_id": item_id}


```

### Response Models

In FastAPI, response models are used to define the structure of the data that will be returned from an API endpoint. This allows you to specify what kind of data a client can expect to receive in response to a request.

```python
class ItemWithoutDescription(BaseModel):
    name:str

class Item(BaseModel):
    name: str
    description: str

@app.get("/items/", response_model=ItemWithoutDescription)
async def read_items():
    # Do something the resposne should be without description
    return items

```

### Status Code Response

```python
from fastapi import FastAPI, HTTPException, Request, status
app = FastAPI()

# POST Create New book
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return {"message": "Book created successfully"}
```

### Work with form DATA

```python
from fastapi import FastAPI, HTTPException, Request, status,Form
app = FastAPI()
# Must install multipart form package
@app.post("/books/login")
async def book_login(username: str = Form(), passsword: str = Form()):
    return {"username": username, "passoord": passsword}
```

### Work with Headers

```python
from fastapi import FastAPI, HTTPException, Request, status,Form,Header
app = FastAPI()

@app.get("/header")
async def get_header(random_header: Optional[str] = Header(None)):
    return {"header": random_header}


```
