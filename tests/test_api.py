import math
from http import HTTPStatus

import pytest
import requests
from fastapi_pagination import paginate, Params
from functions import first
from pydantic import ValidationError

from models.User import ResponseModelList, ResponseModel, ResponseModelListResource, UserDataCreateResponse, \
    UserDataUpdateResponse, UserDataUpdateBody, UserData
from tests.conftest import base_url


@pytest.mark.parametrize("page_number", [2])
def test_api_list_users_status_code_200(base_url, page_number):
    url = f"{base_url}/api/users?page={page_number}"
    response = requests.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("page_number", [
    (2)
])
def test_api_list_users_response_not_empty(base_url, page_number):
    url = f"{base_url}/api/users?page={page_number}"
    response = requests.get(url)
    data = response.json()
    assert len(data['data']) > 0


@pytest.mark.parametrize("page_number", [
    (2)
])
def test_api_list_users_validate_response_schema(base_url, page_number):
    url = f"{base_url}/api/users?page={page_number}"
    headers = {'x-api-key': 'reqres-free-v1'}
    response = requests.get(url, headers=headers)
    ResponseModelList(**response.json())


@pytest.mark.parametrize("user_id", [
    (2)
])
def test_api_single_user_status_code_200(base_url, user_id):
    url = f"{base_url}/api/users/{user_id}"
    headers = {'x-api-key': 'reqres-free-v1'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


@pytest.mark.parametrize("user_id", [
    (2)
])
def test_api_single_user_validate_response_schema(base_url, user_id):
    url = f"{base_url}/api/users/{user_id}"
    headers = {'x-api-key': 'reqres-free-v1'}
    response = requests.get(url, headers=headers)
    ResponseModel(**response.json())


def test_api_list_resource_status_code_200(base_url):
    url = f"{base_url}/api/unknown"
    headers = {'x-api-key': 'reqres-free-v1'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def test_api_list_resource_response_not_empty(base_url):
    url = f"{base_url}/api/unknown"
    headers = {'x-api-key': 'reqres-free-v1'}
    response = requests.get(url, headers=headers)
    data = response.json()
    assert len(data['data']) > 0


def test_api_list_resource_validate_response_schema(base_url):
    url = f"{base_url}/api/unknown"
    headers = {'x-api-key': 'reqres-free-v1'}
    response = requests.get(url, headers=headers)
    ResponseModelListResource(**response.json())


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


@pytest.mark.parametrize("user_id", [
    (2)
])
def test_api_delete_user_status_code_204(base_url, user_id):
    response = requests.delete(url=f"{base_url}/api/users/{user_id}")
    assert response.status_code == 204


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

    assert paginated_data["page"] == page, f"Номер страницы не совпадает. Ожидалось: {page}, получено: {paginated_data['page']}"
    assert paginated_data["size"] == size, f"Размер страницы не совпадает. Ожидалось: {size}, получено: {paginated_data['size']}"
    assert "total" in paginated_data, "Отсутствует общее количество элементов (total)"
    assert "pages" in paginated_data, "Отсутствует общее количество страниц (pages)"

    expected_pages = math.ceil(paginated_data["total"] / size)
    assert paginated_data["pages"] == expected_pages, f"Неверное количество страниц. Ожидалось: {expected_pages}, получено: {paginated_data['pages']}"

    assert len(paginated_data["items"]) == expected_items, f"Неверное количество элементов. Ожидалось: {expected_items}, получено: {len(paginated_data['items'])}"

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

    assert paginated_data["pages"] == expected_pages, f"Количество страниц: ожидается {expected_pages}, получено {paginated_data.pages}"




def test_api_list_users_pagination_different_pages(base_url):
    size = 5
    page1 = 1
    page2 = 2

    response1 = requests.get(f"{base_url}users/?page={page1}&size={size}")
    response2 = requests.get(f"{base_url}users/?page={page2}&size={size}")

    assert response1.status_code == 200
    assert response2.status_code == 200

    items1 = response1.json()["items"]
    items2 = response2.json()["items"]

    assert items1 != items2

    ids1 = {item["id"] for item in items1}
    ids2 = {item["id"] for item in items2}
    intersection = ids1 & ids2
    assert len(intersection) == 0, f"Обнаружены пересекающиеся ID: {intersection}"




# total_items = len(test_data_users)
    # total_pages = math.ceil(total_items / size)
    #
    # if total_pages < 2:
    #     pytest.skip("Недостаточное количество страниц для выполнения проверки")
    #
    # page1 = paginate(test_data_users, params=Params(page=1, size=size))
    # page2 = paginate(test_data_users, params=Params(page=2, size=size))
    #
    # if size < total_items:
    #     assert len(page1.items) > 0, "Первая страница не должна быть пустой"
    #     assert len(page2.items) > 0, "Вторая страница не должна быть пустой"
    #
    # page1_ids = {item['id'] for item in page1.items}
    # page2_ids = {item['id'] for item in page2.items}
    #
    # if page1_ids == page2_ids:
    #     pytest.warn("Страницы содержат одинаковые элементы, возможно, в разном порядке)")
    # else:
    #     assert not (page1_ids.issubset(page2_ids) or page2_ids.issubset(page1_ids)), \
    #         "Одна страница полностью дублирует другую"
    #
    #     if page1.items and page2.items:
    #         try:
    #             assert page1.items[-1]['id'] < page2.items[0]['id'], \
    #                 "Нарушен порядок элементов между страницами"
    #         except AssertionError:
    #             pytest.warn("Нарушен порядок элементов между страницами")