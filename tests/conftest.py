import pytest
import os


@pytest.fixture()
def test_folder():
    test_file_path = os.path.abspath(__file__)
    return os.path.dirname(test_file_path)
