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
        files: Optional[dict] = None
    ):
        if use_json:
            r = httpx.post(url=url, json=data)
        else:
            r = httpx.post(url=url, data=data, files=files)
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
        files: Optional[dict] = None
    ):
        async with httpx.AsyncClient() as client:
            if use_json:
                r = await client.post(url=url, json=data)
            else:
                r = await client.post(url=url, data=data, files=files)
        return r.json()
