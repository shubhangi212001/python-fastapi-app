
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL connection details
MYSQL_USER = "root"
MYSQL_PASSWORD = "support#123"
MYSQL_HOST = "172.16.22.122"  # Remove port from host
MYSQL_PORT = "30300"
MYSQL_DATABASE = "fastapi_mysql"

# MySQL connection URL
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)  # Add pool_pre_ping=True to enable connection health check
# engine.connect()  # No need to explicitly connect here

# Create a sessionmaker to create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Base.metadata.create_all(bind=engine)  # Avoid calling create_all here as it's usually done separately
