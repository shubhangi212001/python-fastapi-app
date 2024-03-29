from pydantic import BaseModel, Field, HttpUrl, AnyHttpUrl

class UserCreate(BaseModel):
    name: str = Field(None, title="Host Id", max_length=20,example="username")
    email: str = Field(None, title="Host Id", max_length=20,example="email")


class WebsiteCreate(BaseModel):
    url: str =  Field(None, title="Host Id", max_length=100,example="website url")
    user_id: int = Field(..., gt=0, lt=100)


class UserUpdate(BaseModel):
    name: str = Field(None, title="Name", max_length=20, example="username")
    email: str = Field(None, title="Email", max_length=50, example="email")

class WebsiteUpdate(BaseModel):
    url: str = Field(None, title="Name", max_length=20, example="email")
