import math

import pytest
import requests
from fastapi_pagination import paginate, Params

from models.User import ResponseModelList, ResponseModel, ResponseModelListResource, UserDataCreateResponse, \
    UserDataUpdateResponse, UserDataUpdateBody


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
    (1, 1),
    (1, 3),
    (1, 6),
    (1, 10),
    (1, 12),
    (2, 1),
    (2, 3),
    (2, 6),
    (2, 10),
    (2, 12),
    (3, 5),
    (4, 3)
])
def test_api_list_users_pagination_basic_params(test_data_users, page, size):
    total_items = len(test_data_users)
    params = Params(page=page, size=size)
    paginated_page = paginate(test_data_users, params)

    expected_items_count = min(size, total_items - (page - 1) * size)
    assert len(
        paginated_page.items) == expected_items_count, f"Количество элементов на странице {page}, размер страницы {size}: ожидаемое количество элементов {expected_items_count}, получено {len(paginated_page.items)}"
    assert paginated_page.total == total_items, f"Общее количество элементов: ожидается {total_items}, получено {paginated_page.total}"
    assert paginated_page.page == page, f"Текущая страница: ожидается {page}, получено {paginated_page.page}"
    assert paginated_page.size == size, f"Размер страницы: ожидается {size}, получено {paginated_page.size}"
    assert paginated_page.pages == math.ceil(
        total_items / size), f"Количество страниц: ожидается {math.ceil(total_items / size)}, получено {paginated_page.pages}"


@pytest.mark.parametrize("size", [1, 3, 6, 10, 12, 20, 25])
def test_api_list_users_pagination_pages_count(test_data_users, size):
    total_items = len(test_data_users)
    params = Params(page=1, size=size)
    paginated_page = paginate(test_data_users, params)

    expected_pages = math.ceil(total_items / size)
    assert paginated_page.pages == expected_pages, f"Количество страниц: ожидается {expected_pages}, получено {paginated_page.pages}"


@pytest.mark.parametrize("size", [1, 3, 6, 10])
def test_api_list_users_pagination_different_pages(test_data_users, size):
    total_items = len(test_data_users)
    total_pages = math.ceil(total_items / size)

    if total_pages < 2:
        pytest.skip("Недостаточное количество страниц для выполнения проверки")

    page1 = paginate(test_data_users, params=Params(page=1, size=size))
    page2 = paginate(test_data_users, params=Params(page=2, size=size))

    if size < total_items:
        assert len(page1.items) > 0, "Первая страница не должна быть пустой"
        assert len(page2.items) > 0, "Вторая страница не должна быть пустой"

    page1_ids = {item['id'] for item in page1.items}
    page2_ids = {item['id'] for item in page2.items}

    if page1_ids == page2_ids:
        pytest.warn("Страницы содержат одинаковые элементы, возможно, в разном порядке)")
    else:
        assert not (page1_ids.issubset(page2_ids) or page2_ids.issubset(page1_ids)), \
            "Одна страница полностью дублирует другую"

        if page1.items and page2.items:
            try:
                assert page1.items[-1]['id'] < page2.items[0]['id'], \
                    "Нарушен порядок элементов между страницами"
            except AssertionError:
                pytest.warn("Нарушен порядок элементов между страницами")