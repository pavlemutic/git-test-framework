import pytest
from unittest.mock import Mock
from src.exceptions import ResponseMismatchError
from src.response import Response


# Mocking a result object for testing
@pytest.fixture
def mock_result():
    mock = Mock()
    mock.stdout = "Line 1: success\nLine 2: error\nLine 3: complete"
    return mock


@pytest.fixture
def response(mock_result):
    return Response(mock_result)


def test_contains_text_found(response):
    assert response.contains("success") is True


def test_contains_text_not_found(response):
    with pytest.raises(ResponseMismatchError, match="Response doesn't contain expected text: 'not found'"):
        response.contains("not found")


def test_has_text_on_line_found(response):
    match = response.has(1, "success")
    assert match is not None
    assert match == True


def test_has_text_on_line_found_regex(response):
    match = response.has(1, "success", is_regex=True)
    assert match is not None
    assert match.group() == "success"


def test_has_text_on_line_not_found(response):
    with pytest.raises(
        ResponseMismatchError, match="Line number '2': 'Line 2: error' doesn't match expected text: 'success'"
    ):
        response.has(2, "success")


def test_has_line_number_out_of_bounds(response):
    with pytest.raises(IndexError, match="Requested line number '5' is out of the response boundaries"):
        response.has(5, "error")


def test_has_negative_line_number(response):
    with pytest.raises(IndexError, match="Requested line number '-1' is out of the response boundaries"):
        response.has(-1, "error")
