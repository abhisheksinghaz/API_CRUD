from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from typing import List
from sqlalchemy.sql.functions import mode
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from . import models, utils
from .database import SessionLocal,engine,get_db
from sqlalchemy.orm import Session
from . import schemas

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


    

my_posts = [{"title":"T1","content":"I am positive content but still marked as False","id":1}]

@app.get("/")
def root():
    return [{"message": "Hello World"},{"message2":"I am message 2"}]

@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)    # adding new post to the database object
    db.commit()         # commiting the newly made changes to the database.
    db.refresh(new_post)    # returning * -- type statement of SQL
    return new_post

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

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

@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
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

@app.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # check if the email already exist.
    user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=HTTP_409_CONFLICT,
        detail="User with email:{} already exist.".format(user.email))

    #hash the password
    #and then save this hashed password as the new password for the user
    user.password = utils.hashing(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)    # adding new post to the database object
    db.commit()         # commiting the newly made changes to the database.
    db.refresh(new_user)    # returning * -- type statement of SQL
    return new_user

@app.get("/users/{id}",response_model=schemas.UserFetchByIdResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    # if the user does not exist
    if not user :
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, 
        detail= "User with id:{} does not exist.".format(id))
    
    return user

