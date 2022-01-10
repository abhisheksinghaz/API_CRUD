import random
from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.types import OptionalInt
from random import randrange
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from . import models
from .database import SessionLocal,engine,get_db
from sqlalchemy.orm import Session
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

class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    

my_posts = [{"title":"T1","content":"I am positive content but still marked as False","id":1}]

@app.get("/posts")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts



# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return posts

@app.get("/")
def root():
    return [{"message": "Hello World"},{"message2":"I am message 2"}]

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) values (%s, %s, %s) returning * """,
    # (create_post_respone.title, create_post_respone.content, create_post_respone.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)    # adding new post to the database object
    db.commit()         # commiting the newly made changes to the database.
    db.refresh(new_post)    # returning * -- type statement of SQL
    return new_post

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts WHERE  id = {}""".format(id))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No post with id:{} exist in the database".format(id))
    return post


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id).first()
    # db.delete(delete_post)
    # db.commit()
    # print(delete_post)
    if not delete_post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail="No post with id:{} exist in the database".format(id))
    db.delete(delete_post)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # db.commit()
    update_post = post_query.first()
    if not update_post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail="No post with id:{} exist in the database".format(id))
    post_query.update(post.dict())
    db.commit()
    return post_query.first()