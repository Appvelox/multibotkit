from json import JSONDecodeError
from typing import Optional

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class BaseHelper:
    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy

    def _get_httpx_request_kwargs(self):
        kwargs = {}
        headers = self._get_request_headers()
        if headers is not None:
            kwargs["headers"] = headers
        if self.proxy is not None:
            kwargs["proxy"] = self.proxy
        return kwargs

    def _get_httpx_client_kwargs(self):
        kwargs = {}
        headers = self._get_request_headers()
        if headers is not None:
            kwargs["headers"] = headers
        if self.proxy is not None:
            kwargs["proxy"] = self.proxy
        return kwargs

    def _get_request_headers(self):
        return None

    def _sync_post(
        self,
        url: str,
        data: Optional[dict] = None,
        use_json: bool = True,
        files: Optional[dict] = None,
    ):
        if use_json:
            return httpx.post(
                url=url, json=data, **self._get_httpx_request_kwargs()
            )
        return httpx.post(
            url=url, data=data, files=files, **self._get_httpx_request_kwargs()
        )

    async def _async_post(
        self,
        url: str,
        data: Optional[dict] = None,
        use_json: bool = True,
        files: Optional[dict] = None,
    ):
        async with httpx.AsyncClient(**self._get_httpx_client_kwargs()) as client:
            if use_json:
                return await client.post(url=url, json=data)
            return await client.post(url=url, data=data, files=files)

    def _sync_stream(self, method: str, url: str):
        return httpx.stream(
            method=method, url=url, **self._get_httpx_request_kwargs()
        )

    def _get_async_client(self):
        return httpx.AsyncClient(**self._get_httpx_client_kwargs())

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)
        | retry_if_exception_type(JSONDecodeError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def _perform_sync_request(
        self,
        url: str,
        data: Optional[dict] = None,
        use_json: bool = True,
        files: Optional[dict] = None,
    ):
        r = self._sync_post(url=url, data=data, use_json=use_json, files=files)
        return r.json()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)
        | retry_if_exception_type(JSONDecodeError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def _perform_async_request(
        self,
        url: str,
        data: Optional[dict] = None,
        use_json: bool = True,
        files: Optional[dict] = None,
    ):
        r = await self._async_post(url=url, data=data, use_json=use_json, files=files)
        return r.json()
