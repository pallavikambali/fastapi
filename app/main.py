
from app.config import Settings
from fastapi.middleware.cors import CORSMiddleware

from .routers import post,user,auth,vote
from fastapi import FastAPI   

settings = Settings()
print(settings.database_username)



origins = ["*"]


# 2. Create FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
# 5. GET root
@app.get("/")
def root():
    return {"message": "welcome to the FastAPI!"}


 

