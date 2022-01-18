from fastapi import Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from starlette.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from app.database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)    # adding new post to the database object
    db.commit()         # commiting the newly made changes to the database.
    db.refresh(new_post)    # returning * -- type statement of SQL
    return new_post

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No post with id:{} exist in the database".format(id))
    return post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not delete_post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                        detail="No post with id:{} exist in the database".format(id))
    db.delete(delete_post)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
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