from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

# v1\Scripts\activate               # to activate the virtual environment in cmd
# uvicorn app.main:app --reload     # to run the server

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

################################## For Connecting to the Postgres databse ########################
import psycopg2
from psycopg2.extras import RealDictCursor
try:
    conn = psycopg2.connect(host= 'localhost',database='fastapi',user='postgres',password='12345',
    cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connection to database established")
except Exception as error:
    print("Couldn't establish the connection with the database")
    print("Error: ",error)
######################################################################################################

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return [{"message": "Hello World"},{"message2":"I am message 2"}]