import urllib3

import requests
import structlog
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from src.config import Config


logger = structlog.get_logger('requester')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Requester:
    def __init__(self, method: str, url: str, **kwargs: dict):
        self.config = Config()
        self.method = method
        self.url = url
        self.kwargs = kwargs

    def __get_session(self):
        session = self.kwargs.pop('session', None)
        if not session:
            session = requests.Session()

        retries = Retry(
            total=self.config.RETRY_MAX,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def __prepare_request(self):
        prepped = requests.Request(
            method=self.method,
            url=self.url,
            **self.kwargs,
        ).prepare()
        logger.debug('request', method=prepped.method, url=prepped.url, body=prepped.body)
        return prepped

    def __submit_request(self, prepped, session):
        rspns = session.send(
            prepped,
            timeout=self.config.TIMEOUT,
            allow_redirects=self.config.ALLOW_REDIRECTS,
            verify=self.config.VERIFY,
            stream=self.config.STREAM,
        )
        logger.debug('response', status_code=rspns.status_code, response=rspns.text)
        return rspns

    def __run(self):
        session = self.__get_session()
        prepped = self.__prepare_request()
        return self.__submit_request(prepped, session)

    @property
    def response(self):
        rspns = self.__run()
        rspns.raise_for_status()
        return rspns
