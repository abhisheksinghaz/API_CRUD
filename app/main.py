import random
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.types import OptionalInt
from random import randrange
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

# v1\Scripts\activate               # to activate the virtual environment in cmd
# uvicorn app.main:app --reload     # to run the server

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
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts

@app.get("/")
def root():
    return [{"message": "Hello World"},{"message2":"I am message 2"}]

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(create_post_respone: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) values (%s, %s, %s) returning * """,
    (create_post_respone.title, create_post_respone.content, create_post_respone.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE  id = {}""".format(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No post with id:{} exist in the database".format(id))
    return post


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = {} returning *""".format(id))
    delete_post = cursor.fetchone()
    conn.commit()
    if not delete_post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail="No post with id:{} exist in the database".format(id))
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s where id = %s returning * """,
    (updated_post.title, updated_post.content, updated_post.published, id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail="No post with id:{} exist in the database".format(id))
    return post