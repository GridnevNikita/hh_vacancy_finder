from unittest.mock import patch, Mock
from src.api import HeadHunterAPI


@patch("src.api.requests.get")
def test_connect_success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    api.connect()

    mock_get.assert_called_once_with("https://api.hh.ru/vacancies")


@patch("src.api.requests.get")
def test_get_vacancies_success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "items": [
            {"name": "Python Developer", "salary": {"from": 100000}, "alternate_url": "example.com"}
        ]
    }
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("python")

    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        params={"text": "python"}
    )

    assert isinstance(vacancies, list)
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"
