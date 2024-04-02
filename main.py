from fastapi import FastAPI, Depends,HTTPException
from typing import List
import crud, models
from schema import UserCreate, WebsiteCreate,UserUpdate,WebsiteUpdate
from database import SessionLocal
from sqlalchemy.orm import Session
from urllib.parse import quote

app = FastAPI()



# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API to add user details
@app.post("/users/")
def create_user(user: UserCreate):
    return crud.create_user(user)

# API to add website details
@app.post("/websites/")
def create_website(website: WebsiteCreate):
    return crud.create_website(website)

# API to scan website for security headers and add vulnerabilities
@app.post("/websites/scan/{website_id}")
def scan_website(website_id: int):
    return crud.scan_website(website_id)

# API to retrieve vulnerabilities of a website by website ID
@app.get("/websites/vulnerabilities/{website_id}")
def get_website_vulnerabilities_by_id(website_id: int):
    return crud.get_website_vulnerabilities_by_id(website_id)

# API to retrieve user details
@app.get("/user/details/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(user_id, db)


# API to retrieve website details
@app.get("/website/details/{website_id}")
def get_website_by_id(website_id: int, db: Session = Depends(get_db)):
    return crud.get_website_by_id(website_id, db)


# API to retrieve website details
@app.get("/website/vulnerabilities/{website_url}")
def get_website_vulnerabilities_by_url(website_url: str, db: Session = Depends(get_db)):

    # Find the website based on the URL
    # print("website_url ***",website_url)
    # First decode
    # Encode the URL manually
    # website_url = website_url.replace(':', '%3A').replace('/', '%2F')

    # Second decode
    # website_url = unquote(website_url)

    # print("website_url  222",website_url)

    return crud.get_website_vulnerabilities_by_url(website_url, db)


# API to edit user details
@app.put("/user/")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(user_id,user_update,db)


# API to edit user details
@app.put("/website/")
def update_website(website_id: int, website_update: WebsiteUpdate, db: Session = Depends(get_db)):
    return crud.update_website(website_id,website_update,db)



# API to delete user details
@app.delete("/user/delete/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(user_id,db)



# API to delete website details
@app.delete("/website/delete/")
def delete_website(website_id: int, db: Session = Depends(get_db)):
    return crud.delete_website(website_id,db)


if __name__ == '__main__':
    uvicorn.run("main:app", host='172.16.22.122', port=8085, log_level="error", reload = True)
    print("running")
