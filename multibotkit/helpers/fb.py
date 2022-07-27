from multibotkit.helpers.base_helper import BaseHelper
from multibotkit.schemas.fb.outgoing import (
    Message,
    PersistentMenu
)


class FBHelper(BaseHelper):

    def __init__(
        self,
        token: str,
        messages_endpoint: str = "https://graph.facebook.com/v14.0/me/messages?access_token=",
        profile_endpoint: str = "https://graph.facebook.com/v14.0/me/messenger_profile?access_token="
    ):
        self.MESSAGES_URL = messages_endpoint + token
        self.PROFILE_URL = profile_endpoint + token


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
