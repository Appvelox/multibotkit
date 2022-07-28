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
from multibotkit.schemas.vk.outgoing import Message


class VKHelper(BaseHelper):

    MESSAGES_URL = "https://api.vk.com/method/messages.send"
    GET_MESSAGES_UPLOAD_SERVER_URL = (
        "https://api.vk.com/method/photos.getMessagesUploadServer"
    )
    SAVE_MESSAGES_PHOTO_URL = "https://api.vk.com/method/photos.saveMessagesPhoto"
    UPLOAD_PHOTO_URL = "https://api.vk.com/method/photos.getMessagesUploadServer"


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

    def syncSendMessage(self, message: Message):
        data = message.dict(exclude_none=True)
        if data.get("keyboard"):
            data["keyboard"] = json.dumps(data["keyboard"], ensure_ascii=False)
        if data.get("template"):
            data["template"] = json.dumps(data["template"], ensure_ascii=False)

        r = self._perform_sync_request(url=self.MESSAGES_URL, data=data)
        return r

    async def asyncSendMessage(self, message: Message):
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
    def syncUploadPhoto(self, photo: BytesIO, file_name: str, server_url: str):
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
    async def asyncUploadPhoto(self, photo: BytesIO, file_name: str, server_url: str):
        files = {"photo": (f"{file_name}", photo)}
        async with httpx.AsyncClient() as client:
            r = await client.post(server_url, files=files)
        return r.json()

    def syncSavePhoto(self, uploaded_photo: dict):
        r = self._perform_sync_request(
            url=self.SAVE_MESSAGES_PHOTO_URL, data={**uploaded_photo}
        )
        return r["response"][0]

    async def asyncSavePhoto(self, uploaded_photo: dict):
        r = await self._perform_async_request(
            url=self.SAVE_MESSAGES_PHOTO_URL, data={**uploaded_photo}
        )
        return r["response"][0]

    def syncGetPhotoAttachment(self, photo, file_name):
        r = self._perform_sync_request(self.UPLOAD_PHOTO_URL, data={})
        url = r["response"]["upload_url"]

        uploaded_photo = self.syncUploadPhoto(photo, file_name, url)
        saved_photo = self.syncSavePhoto(uploaded_photo)

        owner_id = saved_photo['owner_id']
        photo_id = saved_photo['id']
        access_key = saved_photo['access_key']
        attachment = f"photo{owner_id}_{photo_id}_{access_key}"

        return attachment

    async def asyncGetPhotoAttachment(self, photo, file_name):
        r = await self._perform_async_request(self.UPLOAD_PHOTO_URL, data={})
        url = r["response"]["upload_url"]

        uploaded_photo = await self.asyncUploadPhoto(photo, file_name, url)
        saved_photo = await self.asyncSavePhoto(uploaded_photo)

        owner_id = saved_photo['owner_id']
        photo_id = saved_photo['id']
        access_key = saved_photo['access_key']
        attachment = f"photo{owner_id}_{photo_id}_{access_key}"

        return attachment
