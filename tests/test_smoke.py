import pytest
import requests
from http import HTTPStatus

from pydantic import ValidationError

from models.User import UserData


def test_service_availability(base_url):
    response = requests.get(base_url)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND)


@pytest.fixture
def users(base_url):
    response = requests.get(f"{base_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.mark.parametrize("page,size", [
    (1, 5),
    (2, 5),
    (3, 5),
    (1, 1),
    (12, 1),
    (1, 12),
    (1, 15)
])
def test_get_users(base_url: str, page: int, size: int):
    response = requests.get(f"{base_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    paginated_data = response.json()

    for item in paginated_data["items"]:
        try:
            UserData.model_validate(item)
        except ValidationError as e:
            pytest.fail(f"Невалидные данные пользователя: {e}")


def test_get_users_no_duplicates(base_url: str, users: dict):
    response = requests.get(f"{base_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    users_list = users.get('items', [])

    if not users_list:
        raise AssertionError("Список пользователей пуст")

    users_ids = [user["id"] for user in users_list]
    assert len(users_ids) == len(set(users_ids)), "Обнаружены дубликаты идентификаторов пользователей"


@pytest.mark.parametrize("user_id", [2, 7, 12])
def test_get_user(base_url: str, user_id: int):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    print(user)
    UserData.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(base_url: str, user_id: int):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", ["fafaf", "123abc"])
def test_user_invalid_format(base_url: str, user_id: str):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("user_id", [-1, 0])
def test_user_non_positive_id(base_url: str, user_id: int):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
