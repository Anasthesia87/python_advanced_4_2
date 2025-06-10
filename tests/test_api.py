import math
from http import HTTPStatus

import pytest
import requests
from pydantic import ValidationError

from models.User import UserDataCreateResponse, \
    UserDataUpdateResponse, UserDataUpdateBody, UserData
from tests.conftest import base_url


@pytest.mark.parametrize("page_number", [2])
def test_api_list_users_status_code_200(base_url, page_number):
    url = f"{base_url}/api/users?page={page_number}"
    response = requests.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("page,size", [
    (1, 5),
    (2, 5),
    (3, 5),
    (1, 1),
    (12, 1),
    (1, 12),
    (1, 15)
])
def test_api_list_users_response_not_empty(base_url, page, size):
    response = requests.get(f"{base_url}/api/users/?page={page}&size={size}")
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) > 0


@pytest.mark.parametrize("page,size", [
    (1, 5),
    (2, 5),
    (3, 5),
    (1, 1),
    (12, 1),
    (1, 12),
    (1, 15)
])
def test_api_list_users_validate_response(base_url, page, size):
    response = requests.get(f"{base_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    paginated_data = response.json()

    for item in paginated_data["items"]:
        try:
            UserData.model_validate(item)
        except ValidationError as e:
            pytest.fail(f"Невалидные данные пользователя: {e}")


def test_api_create_user_status_code_201(base_url):
    response = requests.post(f"{base_url}/api/users",
                             json={"name": "morpheus", "job": "leader"})
    assert response.status_code == 201


def test_api_create_user_validate_response_schema(base_url):
    response = requests.post(f"{base_url}/api/users",
                             json={"name": "morpheus", "job": "leader"})
    UserDataCreateResponse(**response.json())


def test_api_create_user_attributes_match_expected_values(base_url):
    response = requests.post(f"{base_url}/api/users",
                             json={"name": "morpheus", "job": "leader"})
    data = response.json()
    assert data['name'] == 'morpheus'
    assert data['job'] == 'leader'


@pytest.mark.parametrize("user_id", [
    (2)
])
def test_api_put_update_user_status_code_200(base_url, user_id):
    response = requests.put(url=f"{base_url}/api/users/{user_id}",
                            json={"name": "morpheus", "job": "zion resident"})
    assert response.status_code == 200


@pytest.mark.parametrize("user_id", [
    (2)
])
def test_api_put_update_user_validate_response_schema(base_url, user_id):
    response = requests.put(url=f"{base_url}/api/users/{user_id}",
                            json={"name": "morpheus", "job": "zion resident"})
    UserDataUpdateResponse(**response.json())


@pytest.mark.parametrize("user_id", [
    (2)
])
def test_api_patch_update_user_status_code_200(base_url, user_id):
    response = requests.patch(url=f"{base_url}/api/users/{user_id}",
                              json={"name": "morpheus", "job": "zion resident"})
    assert response.status_code == 200


@pytest.mark.parametrize("user_id", [
    (2)
])
def test_api_patch_update_user_validate_response_schema(base_url, user_id):
    response = requests.patch(url=f"{base_url}/api/users/{user_id}",
                              json={"name": "morpheus", "job": "zion resident"})
    UserDataUpdateBody(**response.json())


@pytest.mark.parametrize("page,size", [
    (1, 5),
    (2, 5),
    (3, 5),
    (1, 1),
    (12, 1),
    (1, 12),
    (1, 15)
])
def test_api_list_users_pagination_basic_params(base_url, test_data_users, page, size):
    response = requests.get(f"{base_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    paginated_data = response.json()
    expected_items = (
        size if (page * size) <= paginated_data["total"] else paginated_data["total"] % size
    )

    assert paginated_data[
               "page"] == page, f"Номер страницы не совпадает. Ожидалось: {page}, получено: {paginated_data['page']}"
    assert paginated_data[
               "size"] == size, f"Размер страницы не совпадает. Ожидалось: {size}, получено: {paginated_data['size']}"
    assert "total" in paginated_data, "Отсутствует общее количество элементов (total)"
    assert "pages" in paginated_data, "Отсутствует общее количество страниц (pages)"

    expected_pages = math.ceil(paginated_data["total"] / size)
    assert paginated_data[
               "pages"] == expected_pages, f"Неверное количество страниц. Ожидалось: {expected_pages}, получено: {paginated_data['pages']}"

    assert len(paginated_data[
                   "items"]) == expected_items, f"Неверное количество элементов. Ожидалось: {expected_items}, получено: {len(paginated_data['items'])}"

    for item in paginated_data["items"]:
        try:
            UserData.model_validate(item)
        except ValidationError as e:
            pytest.fail(f"Невалидные данные пользователя: {e}")


@pytest.mark.parametrize("size", [1, 3, 6, 10, 12, 15])
def test_api_list_users_pagination_pages_count(base_url, test_data_users, size):
    response = requests.get(f"{base_url}/api/users/?size={size}")
    assert response.status_code == HTTPStatus.OK

    paginated_data = response.json()
    total_items = paginated_data["total"]
    expected_pages = math.ceil(total_items / size)

    assert paginated_data[
               "pages"] == expected_pages, f"Количество страниц: ожидается {expected_pages}, получено {paginated_data.pages}"


def test_api_list_users_pagination_different_pages(base_url):
    size = 6
    first_page = 1
    second_page = 2

    first_page_response = requests.get(f"{base_url}/api/users/?page={first_page}&size={size}")
    second_page_response = requests.get(f"{base_url}/api/users/?page={second_page}&size={size}")

    assert first_page_response.status_code == 200
    assert second_page_response.status_code == 200

    items_first_page = first_page_response.json()["items"]
    items_second_page = second_page_response.json()["items"]

    assert items_first_page != items_second_page

    ids_first_page = {item["id"] for item in items_first_page}
    ids_second_page = {item["id"] for item in items_second_page}
    intersection = ids_first_page & ids_second_page
    assert len(intersection) == 0, f"Обнаружены пересекающиеся ID: {intersection}"
