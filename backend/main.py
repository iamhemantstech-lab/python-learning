from fastapi import FastAPI # core framework to build API
from pydantic import BaseModel # defines request, response data structure and validation
from typing import List # defines a list of values

# Note: how to run 
# 1. uvicorn main:app
# 2. uvicorn main:app --reload

app = FastAPI() # instance of fastapi

# pydantic model
class User(BaseModel):
    id: int
    name: str
    city: str
    mobile_no: int

# temporary data to store in this variable due to not connected with mysql
users: List[User] = []


@app.get("/") # this is decorator
def read_root():
    return {"message": "Welcome to API development using FASTAPI."}

@app.get("/users")
def users_list():
    return users

@app.post("/add-users")
def add_user(user: User):
    users.append(user)
    return user

@app.put("/user/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if (user.id == user_id):
            users[index] = updated_user
            return updated_user
    return {"error", "User not found"}

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    return {"error", "User not found"}
