import json
from json import JSONDecodeError
from io import BytesIO
from typing import Optional

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from multibotkit.helpers.base_helper import BaseHelper
from multibotkit.schemas.vk.outgoing import Keyboard, Message


class VKHelper(BaseHelper):

    MESSAGES_URL = "https://api.vk.com/method/messages.send"
    GET_MESSAGES_UPLOAD_SERVER_URL = (
        "https://api.vk.com/method/photos.getMessagesUploadServer"
    )
    SAVE_MESSAGES_PHOTO_URL = "https://api.vk.com/method/photos.saveMessagesPhoto"
    UPLOAD_PHOTO_URL = "https://api.vk.com/method/photos.getMessagesUploadServer"

    class _SendMessageArgumentsError(Exception):
        pass

    def __init__(self, access_token: str, api_version: str):
        self.access_token = access_token
        self.api_version = api_version

    def command(self, json_payload: Optional[str] = None):
        if json_payload is None:
            return ""
        return json.loads(json_payload).get("command")

    def button_code(self, json_payload: str):
        if json_payload is None:
            return ""
        return json.loads(json_payload).get("button")

    def sync_send_message(
        self,
        user_id: int,
        text: Optional[str] = None,
        keyboard: Optional[Keyboard] = None,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        attachment: Optional[str] = None,
        template: Optional[dict] = None,
    ):

        if (text is None) and (attachment is None):
            raise self._SendMessageArgumentsError(
                "One of the arguments text and attachment is required"
            )

        message = Message(
            user_id=user_id,
            message=text,
            keyboard=keyboard,
            lat=lat,
            long=long,
            attachment=attachment,
            template=template,
        )

        data = message.dict(exclude_none=True)
        if data.get("keyboard"):
            data["keyboard"] = json.dumps(data["keyboard"], ensure_ascii=False)
        if data.get("template"):
            data["template"] = json.dumps(data["template"], ensure_ascii=False)

        r = self._perform_sync_request(url=self.MESSAGES_URL, data=data)
        return r

    async def async_send_message(
        self,
        user_id: int,
        text: Optional[str] = None,
        keyboard: Optional[Keyboard] = None,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        attachment: Optional[str] = None,
        template: Optional[dict] = None,
    ):
        if (text is None) and (attachment is None):
            raise self.__SendMessageArgumentsError(
                "One of the arguments text and attachment is required, \
but not both"
            )

        message = Message(
            user_id=user_id,
            message=text,
            keyboard=keyboard,
            lat=lat,
            long=long,
            attachment=attachment,
            template=template,
        )
        data = message.dict(exclude_none=True)
        if data.get("keyboard"):
            data["keyboard"] = json.dumps(data["keyboard"], ensure_ascii=False)
        if data.get("template"):
            data["template"] = json.dumps(data["template"], ensure_ascii=False)

        r = await self._perform_async_request(url=self.MESSAGES_URL, data=data)
        return r

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)
        | retry_if_exception_type(JSONDecodeError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def sync_upload_photo(self, photo: BytesIO, file_name: str, server_url: str):
        files = {"photo": (f"{file_name}", photo)}
        r = httpx.post(server_url, files=files)
        return r.json()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)
        | retry_if_exception_type(JSONDecodeError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def async_upload_photo(self, photo: BytesIO, file_name: str, server_url: str):
        files = {"photo": (f"{file_name}", photo)}
        async with httpx.AsyncClient() as client:
            r = await client.post(server_url, files=files)
        return r.json()

    def sync_save_photo(self, uploaded_photo: dict):
        r = self._perform_sync_request(
            url=self.SAVE_MESSAGES_PHOTO_URL, data={**uploaded_photo}
        )
        return r["response"][0]

    async def async_save_photo(self, uploaded_photo: dict):
        r = await self._perform_async_request(
            url=self.SAVE_MESSAGES_PHOTO_URL, data={**uploaded_photo}
        )
        return r["response"][0]

    def sync_get_photo_attachment(self, photo, file_name):
        r = self._perform_sync_request(self.UPLOAD_PHOTO_URL, data={})
        url = r["response"]["upload_url"]

        uploaded_photo = self.sync_upload_photo(photo, file_name, url)
        saved_photo = self.sync_save_photo(uploaded_photo)

        owner_id = saved_photo["owner_id"]
        photo_id = saved_photo["id"]
        access_key = saved_photo["access_key"]
        attachment = f"photo{owner_id}_{photo_id}_{access_key}"

        return attachment

    async def async_get_photo_attachment(self, photo, file_name):
        r = await self._perform_async_request(self.UPLOAD_PHOTO_URL, data={})
        url = r["response"]["upload_url"]

        uploaded_photo = await self.async_upload_photo(photo, file_name, url)
        saved_photo = await self.async_save_photo(uploaded_photo)

        owner_id = saved_photo["owner_id"]
        photo_id = saved_photo["id"]
        access_key = saved_photo["access_key"]
        attachment = f"photo{owner_id}_{photo_id}_{access_key}"

        return attachment
