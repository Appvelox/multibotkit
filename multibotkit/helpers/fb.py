from json import JSONDecodeError

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from multibotkit.schemas.fb.outgoing import (
    Message,
    PersistentMenu
)


class FBHelper:

    def __init__(
        self,
        token: str,
        messages_endpoint: str = "https://graph.facebook.com/v14.0/me/messages?access_token=",
        profile_endpoint: str = "https://graph.facebook.com/v14.0/me/messenger_profile?access_token="
    ):
        self.MESSAGES_URL = messages_endpoint + token
        self.PROFILE_URL = profile_endpoint + token


    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)
        | retry_if_exception_type(JSONDecodeError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def _perform_sync_request(self, url: str, data: dict):
        r = httpx.post(url=url, json=data)
        return r.json()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)
        | retry_if_exception_type(JSONDecodeError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def _perform_async_request(self, url: str, data: dict):
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url, json=data)
        return r.json()


    def sync_send_message(self, message: Message):
        data = message.json(exclude_none=True)
        r = self._perform_sync_request(url=self.MESSAGES_URL, data=data)
        return r

    async def async_send_message(self, message: Message):
        data = message.json(exclude_none=True)
        r = await self._perform_async_request(url=self.MESSAGES_URL, data=data)
        return r


    def sync_send_get_started(self, payload: str = "GET_STARTED"):
        data = {"get_started": {"payload": payload}}
        r = self._perform_sync_request(url=self.PROFILE_URL, data=data)
        return r

    async def async_send_get_started(self, payload: str = "GET_STARTED"):
        data = {"get_started": {"payload": payload}}
        r = await self._perform_async_request(url=self.PROFILE_URL, data=data)
        return r


    def sync_send_greeting(self, text: str):
        data = {"greeting": [{"locale": "default", "text": text}]}
        r = self._perform_sync_request(self.PROFILE_URL, data=data)
        return r

    async def async_send_greeting(self, text: str):
        data = {"greeting": [{"locale": "default", "text": text}]}
        r = await self._perform_async_request(self.PROFILE_URL, data=data)
        return r


    def sync_send_persistent_menu(self, persistent_menu: PersistentMenu):
        data = persistent_menu.dict(exclude_none=True)
        r = self._perform_sync_request(self.PROFILE_URL, data=data)
        return r

    async def async_send_persistent_menu(self, persistent_menu: PersistentMenu):
        data = persistent_menu.dict(exclude_none=True)
        r = await self._perform_async_request(self.PROFILE_URL, data=data)
        return r
