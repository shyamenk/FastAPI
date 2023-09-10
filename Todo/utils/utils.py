from datetime import datetime, timedelta

from databases import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user_model import Users as UserModel
from passlib.context import CryptContext
from schemas.user_schema import TokenData

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaHlhb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# DB Connection


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


# JWT Token
def validate_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None


def create_access_token(email: str, user_id: int):
    to_encode = {"sub": email, "id": user_id}
    expire = datetime.utcnow() + expiry
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Bcrypt


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# User Authentication
def authenticate_user(email: str, password: str, db):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception()
        token_data = TokenData(email)
        return token_data
    except JWTError:
        raise credentials_exception()


# Custom Exceptions


def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def notfound_exception(message: str):
    return HTTPException(status_code=404, detail=f"{message} not found!")
