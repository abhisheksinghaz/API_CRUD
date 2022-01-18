from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import database,schemas,models,utils

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post('/')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    # print(utils.verify(user_credentials.password, user.password))
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    # create a token and return it
    return {"token":"example token"}