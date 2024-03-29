from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine
import database


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)

    websites = relationship("Website", back_populates="owner")

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="websites")
    vulnerabilities = relationship("Vulnerability", back_populates="website")



class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    name = Column(String)
    description = Column(String)

    website = relationship("Website", back_populates="vulnerabilities")  # Define the relationship to Website



# class Vulnerability(Base):
#     __tablename__ = "vulnerabilities"

#     id = Column(Integer, primary_key=True, index=True)
#     website_id = Column(Integer, ForeignKey("websites.id"))
#     name = Column(String(255))
#     description = Column(String(255))
# engine = create_engine(SQLALCHEMY_DATABASE_URL) 

# Base.metadata.create_all(bind=engine)