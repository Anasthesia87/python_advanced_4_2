from fastapi import FastAPI, HTTPException
from fastapi_pagination import add_pagination
import json
from http import HTTPStatus
import uvicorn
from models.AppStatus import AppStatus
from models.User import UserData, UserDataCreateBody, UserDataUpdateBody, UserDataCreateResponse, \
    UserDataUpdateResponse
from fastapi_pagination import Page, paginate

app = FastAPI()

users_list: list[UserData] = []


@app.get("/api/users", response_model=Page[UserData], status_code=HTTPStatus.OK)
def get_list_users():
    return paginate(users_list)


add_pagination(app)


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users_list):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users_list[user_id - 1]


@app.post("/api/users", response_model=UserDataCreateResponse, status_code=201)
def create_user(user: UserDataCreateBody):
    if not user.name or not user.job:
        raise HTTPException(status_code=400, detail="Name and job are required")

    return {
        "name": user.name,
        "job": user.job,
        "id": "409",
        "createdAt": "2025-05-30T08:46:33.132Z"
    }


@app.put("/api/users/{user_id}", response_model=UserDataUpdateResponse)
def update_user_put(user: UserDataUpdateBody):
    return {
        "name": user.name,
        "job": user.job,
        "updatedAt": "2025-05-30T09:58:46.242Z"
    }


@app.patch("/api/users/{user_id}", response_model=UserDataUpdateResponse)
def update_user_patch(user: UserDataUpdateBody):
    return {
        "name": user.name,
        "job": user.job,
        "updatedAt": "2025-05-30T10:29:24.851Z"
    }


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users_list))


if __name__ == "__main__":
    with open("tests/users.json") as f:
        users_list = json.load(f)

    for user in users_list:
        UserData.model_validate(user)

    print("Users loaded")

    uvicorn.run(app, host="127.0.0.1", port=8001)
