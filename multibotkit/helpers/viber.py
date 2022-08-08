from typing import Optional

from multibotkit.helpers.base_helper import BaseHelper
from multibotkit.schemas.viber.outgoing import (
    Contact,
    Keyboard,
    Location,
    MessageType,
    Sender,
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

    class _SendMessageArgumentsError(Exception):
        pass

    def __init__(self, token):
        self.token = token

    def __build_message(
        self,
        type: MessageType,
        receiver: str,
        min_api_version: int = 7,
        sender: Optional[Sender] = None,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None,
        text: Optional[str] = None,
        media: Optional[str] = None,
        thumbnail: Optional[str] = None,
        size: Optional[int] = None,
        duration: Optional[int] = None,
        file_name: Optional[str] = None,
        contact: Optional[Contact] = None,
        location: Optional[Location] = None,
        sticker_id: Optional[int] = None,
    ):
        if type == "text":
            if text is None:
                raise self._SendMessageArgumentsError(
                    "For text message argument text is required"
                )
            message = TextMessage(
                type=type,
                receiver=receiver,
                min_api_version=min_api_version,
                sender=sender,
                tracking_data=tracking_data,
                keyboard=keyboard,
                text=text,
            )

        if type == "picture":
            if (text is None) or (media is None):
                raise self._SendMessageArgumentsError(
                    "For picture message arguments text and media are required"
                )
            message = PictureMessage(
                type=type,
                receiver=receiver,
                min_api_version=min_api_version,
                sender=sender,
                tracking_data=tracking_data,
                keyboard=keyboard,
                text=text,
                media=media,
                thumbnail=thumbnail,
            )

        if type == "video":
            if (media is None) or (size is None):
                raise self._SendMessageArgumentsError(
                    "For video message arguments media and size are required"
                )
            message = VideoMessage(
                type=type,
                receiver=receiver,
                min_api_version=min_api_version,
                sender=sender,
                tracking_data=tracking_data,
                keyboard=keyboard,
                media=media,
                thumbnail=thumbnail,
                size=size,
                duration=duration,
            )

        if type == "file":
            if (media is None) or (size is None) or (file_name is None):
                raise self._SendMessageArgumentsError(
                    "For file message arguments media, size and file_name \
are required"
                )
            message = FileMessage(
                type=type,
                receiver=receiver,
                min_api_version=min_api_version,
                sender=sender,
                tracking_data=tracking_data,
                keyboard=keyboard,
                media=media,
                size=size,
                file_name=file_name,
            )

        if type == "contact":
            if contact is None:
                raise self._SendMessageArgumentsError(
                    "For contact message argument contact is required"
                )
            message = ContactMessage(
                type=type,
                receiver=receiver,
                min_api_version=min_api_version,
                sender=sender,
                tracking_data=tracking_data,
                keyboard=keyboard,
                contact=contact,
            )

        if type == "location":
            if location is None:
                raise self._SendMessageArgumentsError(
                    "For location message argument location is required"
                )
            message = LocationMessage(
                type=type,
                receiver=receiver,
                min_api_version=min_api_version,
                sender=sender,
                tracking_data=tracking_data,
                keyboard=keyboard,
                location=location,
            )

        if type == "url":
            if media is None:
                raise self._SendMessageArgumentsError(
                    "For url message argument media is required"
                )
            message = UrlMessage(
                type=type,
                receiver=receiver,
                min_api_version=min_api_version,
                sender=sender,
                tracking_data=tracking_data,
                keyboard=keyboard,
                media=media,
            )

        if type == "sticker":
            if sticker_id is None:
                raise self._SendMessageArgumentsError(
                    "For sticker message argument sticker_id is required"
                )
            message = StickerMessage(
                type=type,
                receiver=receiver,
                min_api_version=min_api_version,
                sender=sender,
                tracking_data=tracking_data,
                keyboard=keyboard,
                sticker_id=sticker_id,
            )

        return message

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
        type: MessageType,
        receiver: str,
        min_api_version: int = 7,
        sender: Optional[Sender] = None,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None,
        text: Optional[str] = None,
        media: Optional[str] = None,
        thumbnail: Optional[str] = None,
        size: Optional[int] = None,
        duration: Optional[int] = None,
        file_name: Optional[str] = None,
        contact: Optional[Contact] = None,
        location: Optional[Location] = None,
        sticker_id: Optional[int] = None,
    ):
        message = self.__build_message(
            type=type,
            receiver=receiver,
            min_api_version=min_api_version,
            sender=sender,
            tracking_data=tracking_data,
            keyboard=keyboard,
            text=text,
            media=media,
            thumbnail=thumbnail,
            size=size,
            duration=duration,
            file_name=file_name,
            contact=contact,
            location=location,
            sticker_id=sticker_id,
        )

        url = self.VIBER_BASE_URL + "send_message"
        data = message.dict(exclude_none=True)
        data["auth_token"] = self.token
        r = self._perform_sync_request(url=url, data=data)
        return r

    async def async_send_message(
        self,
        type: MessageType,
        receiver: str,
        min_api_version: int = 7,
        sender: Optional[Sender] = None,
        tracking_data: Optional[str] = None,
        keyboard: Optional[Keyboard] = None,
        text: Optional[str] = None,
        media: Optional[str] = None,
        thumbnail: Optional[str] = None,
        size: Optional[int] = None,
        duration: Optional[int] = None,
        file_name: Optional[str] = None,
        contact: Optional[Contact] = None,
        location: Optional[Location] = None,
        sticker_id: Optional[int] = None,
    ):
        message = self.__build_message(
            type=type,
            receiver=receiver,
            min_api_version=min_api_version,
            sender=sender,
            tracking_data=tracking_data,
            keyboard=keyboard,
            text=text,
            media=media,
            thumbnail=thumbnail,
            size=size,
            duration=duration,
            file_name=file_name,
            contact=contact,
            location=location,
            sticker_id=sticker_id,
        )

        url = self.VIBER_BASE_URL + "send_message"
        data = message.dict(exclude_none=True)
        data["auth_token"] = self.token
        r = await self._perform_async_request(url=url, data=data)
        return r
