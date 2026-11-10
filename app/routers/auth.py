from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils,oauth2
from app.database import get_db


router = APIRouter(tags=["Authentication"]) 


@router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Implement your login logic here
    # For example, you can check the user's credentials in the database
    # and return a token or user information if successful.
    
    
    
    db_user = db.query(models.User).filter(models.User.email == user.username).first()
    if not db_user or not utils.verify(user.password, str(db_user.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}