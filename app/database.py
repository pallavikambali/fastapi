
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# 1. Database configuration
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=int(settings.database_port),
    database=settings.database_name,
)


# 2. Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)

# 3. Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# 4. Create Base class
Base = declarative_base()


# 5. Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# try:
#     connection = psycopg2.connect(
#         host="localhost",
#         database="fastapi",
#         user="postgres",
#         password="761952"
#     )

#     cursor = connection.cursor(cursor_factory=RealDictCursor)

#     print("Database connection was successful!")

# except psycopg2.Error as e:
#     print(f"Error connecting to PostgreSQL: {e}")
#     raise