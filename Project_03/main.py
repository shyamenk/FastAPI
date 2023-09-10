from database import engine
from fastapi import FastAPI
from models import Base
from routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router=router)
