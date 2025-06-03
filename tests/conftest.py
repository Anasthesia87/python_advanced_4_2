import dotenv
import pytest

BASE_URL = "http://127.0.0.1:8001"

@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def base_url():
    return BASE_URL