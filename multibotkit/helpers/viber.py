from typing import Union

from multibotkit.helpers.base_helper import BaseHelper
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


class ViberHelper(BaseHelper):

    VIBER_BASE_URL = "https://chatapi.viber.com/pa/"

    def __init__(self, token):
        self.token = token

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
