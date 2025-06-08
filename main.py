from fastapi import FastAPI, HTTPException, Depends
from fastapi_pagination import Params
import json
from http import HTTPStatus
from fastapi.responses import Response
import uvicorn
from models.AppStatus import AppStatus
from models.User import UserData, UserDataCreateBody, UserDataUpdateBody, UserDataCreateResponse, \
    UserDataUpdateResponse, ResponseModel, ResponseModelList, ResponseModelListResource, ResourceData
from fastapi_pagination import Page, paginate
from data.users_data import users_with_page
from data.resources_data import resources_with_page

app = FastAPI()

users_list: list[UserData] = []
resources_list: list[ResourceData] = []



@app.get("/api/users", response_model=ResponseModelList)
def get_list_users(page: int = 2):
    user_data = users_with_page.get(page)
    if not user_data:
        raise HTTPException(status_code=404, detail="Page not found")

    return user_data


@app.get("/api/users/{user_id}", response_model=ResponseModel)
def get_single_user(user_id: int):
    for page_data in users_with_page.values():
        for user in page_data["data"]:
            if user["id"] == user_id:
                return {"data": user,
                        "support": page_data["support"]}

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/api/unknown", response_model=ResponseModelListResource)
def get_list_resource():
    resource_data = resources_with_page.get(1)
    if not resource_data:
        raise HTTPException(status_code=404, detail="Resource not found")

    return {
        "page": resource_data["page"],
        "per_page": resource_data["per_page"],
        "total": resource_data["total"],
        "total_pages": resource_data["total_pages"],
        "data": resource_data["data"],
        "support": resource_data["support"],
    }


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


@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_with_page:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(status_code=204)


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users_with_page))


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users_list):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users_list[user_id - 1]


@app.get("/api/users/", status_code=HTTPStatus.OK)
def get_users() -> list[UserData]:
    return users_list


@app.get("/api/users", response_model=Page[UserData])
def get_list_users_with_pagination(params: Params = Depends()):
    return paginate(users_list, params)


@app.get("/api/unknown", response_model=Page[ResourceData])
def get_list_resources_with_pagination(params: Params = Depends()):
    return paginate(resources_list, params)


if __name__ == "__main__":
    with open("tests/users.json") as f:
        users_list = json.load(f)

    for user in users_list:
        UserData.model_validate(user)

    print("Users loaded")

    uvicorn.run(app, host="127.0.0.1", port=8001)
