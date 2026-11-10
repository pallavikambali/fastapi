from .. import models, schemas,oauth2
from fastapi import FastAPI,HTTPException, status, Depends, Response,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List


router = APIRouter(
    prefix="/posts",  # Prefix for all routes in this router
    tags=["Posts"]  # Tag for grouping routes in the documentat ion
)



@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),limit: int = 10,search: str = "",skip: int = 0):

    print(limit)
    #posts = cursor.execute("SELECT * FROM public.posts")
    #posts=cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("vote_count")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts




# 8. POST - create a post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)  
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute(
    #   "INSERT INTO public.posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #  (post.title, post.content, post.published)
    #)   
    #new_post = cursor.fetchone()
    #connection.commit()
    print(current_user.id)
    print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# 9. GET - search posts
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)  ):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    #print("Current user ID:", current_user.id)
    post = db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post      



# 10. DELETE - delete a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    

    db.delete(post)
    db.commit()


# 11. PUT - update a post
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute(
    #    "UPDATE public.posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #    (updated_post.title, updated_post.content, updated_post.published, id)
    #)
    #post = cursor.fetchone()
    #connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    

    if post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action",
            )
    post_query.update(
    {
        models.Post.title: updated_post.title,
        models.Post.content: updated_post.content,
        models.Post.published: updated_post.published,
    },
    synchronize_session=False
)
    db.commit()
    db.refresh(post)
    return post