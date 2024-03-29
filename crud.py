from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal,engine
import requests
from schema import UserCreate, WebsiteCreate,UserUpdate,WebsiteUpdate
from models import Website, Vulnerability
from urllib.parse import quote


# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def create_user(user: UserCreate, db: Session = None):
    db = db or SessionLocal()
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def create_website(website: WebsiteCreate, db: Session = None):
    db = db or SessionLocal()
    db_website = models.Website(url=website.url, user_id=website.user_id)
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    return db_website

# Function to scan website for security headers and add vulnerabilities
def scan_website(website_id: int, db: Session = None):
    db = db or SessionLocal()
    website = db.query(models.Website).filter(models.Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    # Call function to scan website for security headers
    vulnerabilities = check_security_headers(website.url, website_id, db)

    return {"website_id": website_id, "vulnerabilities": vulnerabilities}


# Function to retrieve vulnerabilities of a website by website ID
def get_website_vulnerabilities_by_id(website_id: int, db: Session = None):
    db = db or SessionLocal()
    return db.query(models.Vulnerability).filter(models.Vulnerability.website_id == website_id).all()


def get_user_by_id(user_id: int, db: Session = None):
    db = db or SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

def get_website_by_id(website_id: int, db: Session = None):
    # db = db or SessionLocal()
    user = db.query(models.Website).filter(models.Website.id == website_id).first()
    return user


def get_website_vulnerabilities_by_url(website_url: str, db: Session):
    # Find the website based on the URL
    
    # Second decode
    # website_url = unquote(website_url)

    # print("website_url  2",website_url)

    website = db.query(models.Website).filter(models.Website.url == website_url).first()
    print("website url ",website.url)
    print("rrr",website)
    if website:
        # If the website is found, retrieve vulnerabilities associated with its ID
        vulnerabilities = db.query(models.Vulnerability).filter(models.Vulnerability.website_id == website.id).all()
        return vulnerabilities
    else:
        return None  # Return None if website with the given URL is not found



def update_user(user_id: int, user_update: UserUpdate, db: Session = None):

    db = db or SessionLocal()
    try:
        # Query the user by id
        user_to_update = db.query(models.User).filter(models.User.id == user_id).first()

        # Update user details
        if user_to_update:
            if user_update.name:
                user_to_update.name = user_update.name
            if user_update.email:
                user_to_update.email = user_update.email

            db.add(user_to_update)
            # Commit the changes to the database
            db.commit()
            print("User details updated successfully.")
            print(user_to_update)
            data = [{'name': user_update.name,
             'email': user_update.email}]
            return data 
        else:
            print("User not found.")
            return False
    except Exception as e:
        print(f"Error updating user details: {e}")
        return False
    # finally:
    #     # Close the session
    #     db.close()



def update_website(websit_id: int, websit_update: WebsiteUpdate, db: Session = None):

    db = db or SessionLocal()
    try:
        # Query the user by id
        websit_to_update = db.query(models.Website).filter(models.Website.id == websit_id).first()

        # Update user details
        if websit_to_update:
            if websit_update.url:
                websit_to_update.url = websit_update.url

            db.add(websit_to_update)
            # Commit the changes to the database
            db.commit()
            print("Website details updated successfully.")
            print(websit_to_update)
            data = [{'url': websit_update.url
             }]
            return data 
        else:
            print("website not found.")
            return False
    except Exception as e:
        print(f"Error updating user details: {e}")
        return False
    # finally:
    #     # Close the session
    #     db.close()



def delete_user(user_id: int, db: Session = None):
    """
    Delete a user by ID.
    """
    db = db or SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def delete_website(website_id: int, db: Session = None):
    """
    Delete a user by ID.
    """
    db = db or SessionLocal()
    website = db.query(models.Website).filter(models.Website.id == website_id).first()
    if website is None:
        return False

    # Delete associated vulnerabilities
    db.query(models.Vulnerability).filter(models.Vulnerability.website_id == website_id).delete()

    # Delete the website
    db.delete(website)
    db.commit()
    return True
    



# Function to scan website for security headers
def check_security_headers(website_url: str, website_id: int, db: Session):
    headers = requests.get(website_url).headers
    vulnerabilities = []
    for header, value in headers.items():
        if header.lower().startswith('x-') or header.lower().startswith('content-'):
            vulnerability = models.Vulnerability(name=header, description=f"Header value: {value}", website_id=website_id)
            db.add(vulnerability)
            vulnerabilities.append(vulnerability)
    db.commit()
    return vulnerabilities





