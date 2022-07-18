import httpx

from multibotkit.schemas.fb.outgoing_messages import Message


class FBHelper:
    def __init__(self, messages_endpoint: str, profile_endpoint: str, token: str):
        self.MESSAGES_URL = messages_endpoint + token
        self.PROFILE_URL = profile_endpoint + token

    def _perform_sync_request(self, url: str, data: dict):
        r = httpx.post(url=url, json=data)
        return r

    async def _perform_async_request(self, url: str, data: dict):
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url, json=data)
        return r

    def sync_send_message(self, message: Message):
        data = message.json(exclude_none=True)
        r = self._perform_sync_request(url=self.MESSAGES_URL, data=data)
        return r.json()

    async def async_send_message(self, message: Message):
        data = message.json(exclude_none=True)
        r = await self._perform_async_request(url=self.MESSAGES_URL, data=data)
        return r.json()

    def sync_send_get_started(self):
        data = {"get_started": {"payload": "GET_STARTED"}}
        r = self._perform_sync_request(url=self.PROFILE_URL, data=data)
        return r.json()

    async def async_send_get_started(self):
        data = {"get_started": {"payload": "GET_STARTED"}}
        r = await self._perform_async_request(url=self.PROFILE_URL, data=data)
        return r.json()

    def sync_send_greeting(self):
        data = {"greeting": [{"locale": "default", "text": "Привет!"}]}
        r = self._perform_sync_request(self.PROFILE_URL, json=data)
        return r.json()

    async def async_send_greeting(self):
        data = {"greeting": [{"locale": "default", "text": "Привет!"}]}
        r = await self._perform_async_request(self.PROFILE_URL, data=data)
        return r.json()

    def sync_send_persistent_menu(self):
        data = {
            "persistent_menu": [{"locale": "default", "composer_input_disabled": False}]
        }
        r = self._perform_sync_request(self.PROFILE_URL, data=data)
        return r.json()

    async def async_send_persistent_menu(self):
        data = {
            "persistent_menu": [{"locale": "default", "composer_input_disabled": False}]
        }
        r = await self._perform_async_request(self.PROFILE_URL, data=data)
        return r.json()
