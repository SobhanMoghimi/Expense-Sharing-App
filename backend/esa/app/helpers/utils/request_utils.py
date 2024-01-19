import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from mmb.app.models.dtos.dtos import RequestDTO
from mmb.app.models.enums import RequestMethod


class RequestUtils:
    @classmethod
    def request_with_retry(
        cls,
        request_model: RequestDTO,
    ):
        session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=request_model.max_retry,
                backoff_factor=request_model.backoff_factor,
                allowed_methods=None,
                status_forcelist=[429, 500, 502, 503, 504],
            ),
        )
        session.mount("http", adapter)
        session.mount("https", adapter)

        try:
            match request_model.method:
                case RequestMethod.GET:
                    return session.get(request_model.url, headers=request_model.headers, params=request_model.params)
                case RequestMethod.POST:
                    return session.post(request_model.url, headers=request_model.headers, data=request_model.data)
                case _:
                    raise NotImplementedError
        except Exception as e:
            return e

    @classmethod
    def check_connectivity(cls, url: str) -> bool:
        try:
            is_connected = requests.head(url, timeout=2)
            return is_connected.status_code == 200
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            return False