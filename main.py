from fastapi import FastAPI

from databases.database import Base, engine
from routes import address_rote, auth_route, todo_route, user_route

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(address_rote.router)
app.include_router(todo_route.router)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=3500, workers=4, reload=True)
