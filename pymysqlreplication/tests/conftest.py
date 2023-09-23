import pytest


def pytest_addoption(parser):
    parser.addoption("--dbms", action="store", default="mysql-5")


@pytest.fixture
def get_dbms(request):
    return request.config.getoption("--dbms")
