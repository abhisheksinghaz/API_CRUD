import random
# from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.types import OptionalInt
from random import randrange

from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = False
    rating: OptionalInt

my_posts = [{"title":"T1","content":"I am positive content but still marked as False","id":1},
{"title":"T2","content":"I am Purely positive","publish":True,"id":2}]

@app.get("/posts")
def get_posts():
    # this is a GET request
    # my_posts.sort(id)
    # print(my_posts)
    # # my_posts.sort()
    # print(my_posts)
    return my_posts

@app.get("/")
def root():
    return [{"message": "Hello World"},{"message2":"I am message 2"}]

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(create_post_respone: Post):
    post_dict = create_post_respone.dict()
    post_dict["id"] = random.randrange(1,1000)
    my_posts.append(post_dict)
    # this is a POST request
    return post_dict

def find_post(id):
    for index,post in enumerate(my_posts):
        # print(post,type(post["id"]))
        if post["id"] == id:
            return [index,post]

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No post with id:{} exist in the database".format(id))
    return post[1]


@app.delete("/posts/{id}")
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail="No post with id:{} exist in the database".format(id))

    my_posts.pop(post[0])
    return Response(status_code=HTTP_204_NO_CONTENT)