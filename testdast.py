import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define Pydantic models for User, Website, and Vulnerability
class User(BaseModel):
    id: int
    name: str
    email: str

class Website(BaseModel):
    id: int
    url: str
    user_id: int

class Vulnerability(BaseModel):
    id: int
    website_id: int
    name: str
    description: str

# In-memory database
users_db = []
websites_db = []
vulnerabilities_db = []

# Function to scan website for security headers and add vulnerabilities
def scan_website_for_security_headers(website_id: int, website_url: str):
    headers = requests.get(website_url).headers
    vulnerabilities = []
    for header, value in headers.items():
        if header.lower().startswith('x-') or header.lower().startswith('content-'):
            vulnerability = Vulnerability(
                id=len(vulnerabilities_db) + 1,
                website_id=website_id,
                name=header,
                description=f"Header value: {value}"
            )
            vulnerabilities_db.append(vulnerability)
            vulnerabilities.append(vulnerability)
    return vulnerabilities

# API to add user details
@app.post("/users/", response_model=User)
def create_user(user: User):
    users_db.append(user)
    return user

# API to add website details
@app.post("/websites/", response_model=Website)
def create_website(website: Website, user_id: int):
    website.user_id = user_id
    websites_db.append(website)
    return website

# API to scan website for security headers and add vulnerabilities
@app.post("/websites/{website_id}/scan/")
def scan_website(website_id: int):
    website = next((w for w in websites_db if w.id == website_id), None)
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    website_url = website.url
    vulnerabilities = scan_website_for_security_headers(website_id, website_url)
    
    return {"website_id": website_id, "vulnerabilities": vulnerabilities}

# API to retrieve vulnerabilities of a website by website ID
@app.get("/websites/{website_id}/vulnerabilities/", response_model=List[Vulnerability])
def get_website_vulnerabilities_by_id(website_id: int):
    website_vulnerabilities = [v for v in vulnerabilities_db if v.website_id == website_id]
    return website_vulnerabilities
