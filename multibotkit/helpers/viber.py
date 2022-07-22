from json import JSONDecodeError
from typing import Union

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from multibotkit.schemas.viber.outgoing import (
    SetWebhook,
    StickerMessage,
    UrlMessage,
    LocationMessage,
    ContactMessage,
    FileMessage,
    VideoMessage,
    PictureMessage,
    TextMessage,
)


class ViberHelper:

    VIBER_BASE_URL = "https://chatapi.viber.com/pa/"

    def __init__(self, token):
        self.token = token

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)
        | retry_if_exception_type(JSONDecodeError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def _perform_sync_request(self, url: str, data: dict = None):
        r = httpx.post(url=url, json=data)
        return r.json()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)
        | retry_if_exception_type(JSONDecodeError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def _perform_async_request(self, url: str, data: dict = None):
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=data)
            return r.json()

    def sync_set_webhook(self, webhook_data: SetWebhook):
        url = self.VIBER_BASE_URL + "set_webhook"
        data = webhook_data.dict(exclude_none=True)
        data["auth_token"] = self.token
        r = self._perform_sync_request(url=url, data=data)
        return r

    async def async_set_webhook(self, webhook_data: SetWebhook):
        url = self.VIBER_BASE_URL + "set_webhook"
        data = webhook_data.dict(exclude_none=True)
        data["auth_token"] = self.token
        r = await self._perform_async_request(url=url, data=data)
        return r

    def sync_get_account_info(self):
        url = self.VIBER_BASE_URL + "get_account_info"
        r = self._perform_sync_request(url=url)
        return r

    async def async_get_account_info(self):
        url = self.VIBER_BASE_URL + "get_account_info"
        r = await self._perform_async_request(url=url)
        return r

    def sync_send_message(
        self,
        message: Union[
            StickerMessage,
            UrlMessage,
            LocationMessage,
            ContactMessage,
            FileMessage,
            VideoMessage,
            PictureMessage,
            TextMessage,
        ],
    ):
        url = self.VIBER_BASE_URL + "send_message"
        data = message.dict(exclude_none=True)
        data["auth_token"] = self.token
        r = self._perform_sync_request(url=url, data=data)
        return r

    async def async_send_message(
        self,
        message: Union[
            StickerMessage,
            UrlMessage,
            LocationMessage,
            ContactMessage,
            FileMessage,
            VideoMessage,
            PictureMessage,
            TextMessage,
        ],
    ):
        url = self.VIBER_BASE_URL + "send_message"
        data = message.dict(exclude_none=True)
        data["auth_token"] = self.token
        r = await self._perform_async_request(url=url, data=data)
        return r
