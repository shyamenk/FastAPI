## Database connection using sqlite with SqlAlchemy

### Main.py file

```python
from database import engine
from fastapi import FastAPI
from models import Base
from routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router=router)

```

### Connecting to database sqlite

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE = "sqlite:///./todos.db"

engine = create_engine(
    SQL_ALCHEMY_DATABASE,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

```

### Create Models using SQL-Alchemy (ORM)

```python
from database import Base
from sqlalchemy import Boolean, Column, Integer, String


class Todo(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    is_complete = Column(Boolean, default=False)


```

### Create Schema with Pydantic Base Model

```python
from typing import Optional

from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="Priority Must be 0 to 5")
    is_complete: bool

```

### Create Routes with DB_Session for TODO APP with FAST API

```python
from fastapi import APIRouter

router = APIRouter()
def create_db_session():
    try:
        print("Connecting to Database....")
        db_session = SessionLocal()
        yield db_session
    except Exception as e:
        print(f"Error accessing the database: {e}")
        raise
    finally:
        db_session.close()
        print("Database session closed successfully.")

@router.get("/")
async def get_all_todos(db: Session = Depends(create_db_session)):
    todos = db.query(Todo_model).all()
    if todos is None:
        raise http_notfound_exception()
    return todos


```

## JSON Web Tokens (JWT)

JSON Web Tokens (JWT) are a compact, URL-safe means of representing claims to be transferred between two parties. These claims are often used to authenticate the user, share information about them, and in some cases, authorize certain action

### JWT Structure:

- `Header`: Contains information about how the JWT is encoded, including the type (JWT) and the signing algorithm being used (HMAC SHA256 or RSA). BASE 64

- `Payload`: Contains the claims. Claims are statements about an entity (typically, the user) and additional data. There are three types of claims:

  - Registered: iss-> Issuer; sub -> Subject ; exp -> expirartion
  - Public,
  - Private,

- `Signature`: To create the signature part, you have to take the encoded header, the encoded payload, a secret, the algorithm specified in the header, and sign that.

### Example JWT

```json
//Header
{
  "alg": "HS256",
  "typ": "JWT"
}

// JWT Payload

{
    "sub":"12345678",
    "name":"shyam",
    "email":"shyamenk@gmail.com",
    "admin":"true"
}

```

```js
// JWT Signature

HMACSHA256(
  base64urlEncoded(Header) + "." + base64urlEncode(Payload),
  learnonline
);
```

### Example JSON Web Token

```js
JSON_WEB_TOKEN =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6InNoeWFtZW5rIiwiZW1haWwiOiJzaHlhbWVua0BnbWFpbC5jb20iLCJpYXQiOjE1MTYyMzkwMjJ9.f-tY7qVXFmintMRiqAUtnHhz6aVJZZMhkTNI9CH0Wkk";
```
