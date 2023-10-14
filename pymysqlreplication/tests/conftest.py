import pytest


def pytest_addoption(parser):
    parser.addoption("--db", action="store", default="mysql-5")


@pytest.fixture
def get_db(request):
    return request.config.getoption("--db")
