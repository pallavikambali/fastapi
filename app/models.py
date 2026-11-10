
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String,func
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Post(Base):

    __tablename__ = "posts"

    # Unique ID for every post
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # Title of the post
    title: Mapped[str] = mapped_column(String, nullable=False)

    # Content of the post
    content: Mapped[str] = mapped_column(String, nullable=False)

    # Published status of the post
    published = Column(Boolean, default=True,nullable=False )
    #email = Column(String, unique=True, index=True, nullable=False)

    # Stores the hashed password
    #password = Column(String, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(
    Integer,
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="posts")
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    posts = relationship("Post", back_populates="owner")
    

class Vote(Base):   
    
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)