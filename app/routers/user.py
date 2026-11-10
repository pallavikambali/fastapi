from .. import models, schemas, utils
from fastapi import FastAPI,HTTPException, status, Depends, Response,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",  # Prefix for all routes in this router
    tags=["Users"]  # Tag for grouping routes in the documentation
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut )
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
