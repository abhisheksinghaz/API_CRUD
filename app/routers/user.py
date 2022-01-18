from fastapi import status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, utils, models
from app.database import get_db
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
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

@router.get("/{id}",response_model=schemas.UserFetchByIdResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    # if the user does not exist
    if not user :
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, 
        detail= "User with id:{} does not exist.".format(id))
    
    return user