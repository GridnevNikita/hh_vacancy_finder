from unittest.mock import patch, Mock
from src.api import HeadHunterAPI


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

    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"

    assert mock_get.call_count == 2

    args, kwargs = mock_get.call_args_list[1]
    assert kwargs["params"] == {"text": "python", "per_page": 20}
