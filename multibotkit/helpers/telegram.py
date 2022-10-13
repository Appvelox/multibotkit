from io import BytesIO
import json
from typing import IO, Optional, Union, List

import aiofiles
import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from multibotkit.helpers.base_helper import BaseHelper
from multibotkit.schemas.telegram.outgoing import (
    EditMessageMediaModel,
    InlineKeyboardMarkup,
    InputMedia,
    InputMediaPhoto,
    Message,
    Photo,
    ReplyKeyboardMarkup,
    SetWebhookParams,
    WebhookInfo,
    MediaGroup,
)


class TelegramHelper(BaseHelper):
    """
    Sync and async functions for Telegram Bot API
    """

    def __init__(self, token):
        self.token = token
        self.tg_base_url = f"https://api.telegram.org/bot{self.token}/"

    def sync_get_webhook_info(self) -> Optional[WebhookInfo]:
        url = self.tg_base_url + "getWebhookInfo"
        r = self._perform_sync_request(url)
        if r["ok"] is True:
            return WebhookInfo(**r["result"])
        return None

    async def async_get_webhook_info(self) -> Optional[WebhookInfo]:
        url = self.tg_base_url + "getWebhookInfo"
        r = await self._perform_async_request(url)
        if r["ok"] is True:
            return WebhookInfo(**r["result"])
        return None

    def sync_set_webhook(self, webhook_url: str):
        url = self.tg_base_url + "setWebhook"
        params = SetWebhookParams(url=webhook_url)
        data = params.dict(exclude_none=True)
        r = self._perform_sync_request(url, data)
        return r

    async def async_set_webhook(self, webhook_url: str):
        url = self.tg_base_url + "setWebhook"
        params = SetWebhookParams(url=webhook_url)
        data = params.dict(exclude_none=True)
        r = await self._perform_async_request(url, data)
        return r

    def sync_send_message(
        self,
        chat_id: int,
        text: str,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        parse_mode: str = "HTML",
    ):
        url = self.tg_base_url + "sendMessage"
        message = Message(
            chat_id=chat_id,
            text=text,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
        )

        data = message.dict(exclude_none=True)
        data.update({"parse_mode": parse_mode})
        r = self._perform_sync_request(url, data)
        return r

    async def async_send_message(
        self,
        chat_id: int,
        text: str,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        parse_mode: str = "HTML",
    ):
        url = self.tg_base_url + "sendMessage"
        message = Message(
            chat_id=chat_id,
            text=text,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
        )

        data = message.dict(exclude_none=True)
        data.update({"parse_mode": parse_mode})
        r = await self._perform_async_request(url, data)
        return r

    def sync_answer_callback_query(self, callback_query_id: str):
        url = self.tg_base_url + "answerCallbackQuery"
        data = {"callback_query_id": callback_query_id}
        r = self._perform_sync_request(url, data)
        return r

    async def async_answer_callback_query(self, callback_query_id: str):
        url = self.tg_base_url + "answerCallbackQuery"
        data = {"callback_query_id": callback_query_id}
        r = await self._perform_async_request(url, data)
        return r

    def sync_edit_message_text(self, chat_id: int, message_id: int, text: str):
        url = self.tg_base_url + "editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        r = self._perform_sync_request(url, data)
        return r

    async def async_edit_message_text(self, chat_id: int, message_id: int, text: str):
        url = self.tg_base_url + "editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        r = await self._perform_async_request(url, data)
        return r

    def sync_edit_message_caption(self, chat_id: int, message_id: int, caption: str):
        url = self.tg_base_url + "editMessageCaption"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": "Markdown",
        }
        r = self._perform_sync_request(url, data)
        return r

    async def async_edit_message_caption(
        self, chat_id: int, message_id: int, caption: str
    ):
        url = self.tg_base_url + "editMessageCaption"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": "Markdown",
        }
        r = await self._perform_async_request(url, data)
        return r

    def sync_edit_message_reply_markup(
        self,
        chat_id: int,
        message_id: int,
        reply_markup: Optional[InlineKeyboardMarkup],
    ):
        url = self.tg_base_url + "editMessageReplyMarkup"
        try:
            data = {
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": reply_markup.dict(exclude_none=True),
            }
        except AttributeError:
            data = {"chat_id": chat_id, "message_id": message_id, "reply_markup": {}}
        r = self._perform_sync_request(url, data)
        return r

    async def async_edit_message_reply_markup(
        self,
        chat_id: int,
        message_id: int,
        reply_markup: Optional[InlineKeyboardMarkup],
    ):
        url = self.tg_base_url + "editMessageReplyMarkup"
        try:
            data = {
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": reply_markup.dict(exclude_none=True),
            }
        except AttributeError:
            data = {"chat_id": chat_id, "message_id": message_id, "reply_markup": {}}
        r = await self._perform_async_request(url, data)
        return r
    
    def sync_edit_message_media(
        self,
        media: Union[str, IO],
        media_type: str,
        caption: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[Union[int, str]] = None
    ):
        if type(media) == str:
            if media.startswith("http://") or media.startswith("https://"):
                media_obj = InputMedia(
                    type=media_type,
                    media=media,
                    caption=caption
                )
                data_obj = EditMessageMediaModel(
                    chat_id=chat_id,
                    message_id=message_id,
                    inline_message_id=inline_message_id,
                    media=media_obj,
                    reply_markup=reply_markup
                )

                url = self.tg_base_url + "editMessageMedia"
                data = data_obj.dict(exclude_none=True)

                r = self._perform_sync_request(url, data)
                return r
            
            ends = [".jpg", ".jpeg", ".gif", ".png"]
            for end in ends:
                if media.endswith(end):
                    opened_media = open(media, "rb")

                    media_obj = InputMedia(
                        type=media_type,
                        media=f"attach://{media}",
                        caption=caption
                    )
                    data_obj = EditMessageMediaModel(
                        chat_id=chat_id,
                        message_id=message_id,
                        inline_message_id=inline_message_id,
                        media=media_obj,
                        reply_markup=reply_markup
                    )

                    url = self.tg_base_url + "editMessageMedia"
                    data = data_obj.dict(exclude_none=True)
                    files = {media: opened_media}

                    r = self._perform_sync_request(url, data, files=files)
                    return r
            
            media_obj = InputMedia(
                type=media_type,
                media=media,
                caption=caption
            )
            data_obj = EditMessageMediaModel(
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                media=media_obj,
                reply_markup=reply_markup
            )

            url = self.tg_base_url + "editMessageMedia"
            data = data_obj.dict(exclude_none=True)

            r = self._perform_sync_request(url, data)
            return r
        
        media_obj = InputMedia(
            type=media_type,
            media="attach://media",
            caption=caption
        )
        data_obj = EditMessageMediaModel(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            media=media_obj,
            reply_markup=reply_markup
        )

        url = self.tg_base_url + "editMessageMedia"
        data = data_obj.dict(exclude_none=True)
        files = {"media": media}

        r = self._perform_sync_request(url, data, files=files)
        return r
    

    async def async_edit_message_media(
        self,
        media: Union[str, IO],
        media_type: str,
        caption: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[Union[int, str]] = None
    ):
        if type(media) == str:
            if media.startswith("http://") or media.startswith("https://"):
                media_obj = InputMedia(
                    type=media_type,
                    media=media,
                    caption=caption
                )
                data_obj = EditMessageMediaModel(
                    chat_id=chat_id,
                    message_id=message_id,
                    inline_message_id=inline_message_id,
                    media=media_obj,
                    reply_markup=reply_markup
                )

                url = self.tg_base_url + "editMessageMedia"
                data = data_obj.dict(exclude_none=True)

                r = await self._perform_async_request(url, data)
                return r
            
            ends = [".jpg", ".jpeg", ".gif", ".png"]
            for end in ends:
                if media.endswith(end):
                    opened_media = open(media, "rb")

                    media_obj = InputMedia(
                        type=media_type,
                        media=f"attach://{media}",
                        caption=caption
                    )
                    data_obj = EditMessageMediaModel(
                        chat_id=chat_id,
                        message_id=message_id,
                        inline_message_id=inline_message_id,
                        media=media_obj,
                        reply_markup=reply_markup
                    )

                    url = self.tg_base_url + "editMessageMedia"
                    data = data_obj.dict(exclude_none=True)
                    files = {media: opened_media}

                    r = await self._perform_async_request(url, data, files=files)
                    return r
            
            media_obj = InputMedia(
                type=media_type,
                media=media,
                caption=caption
            )
            data_obj = EditMessageMediaModel(
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                media=media_obj,
                reply_markup=reply_markup
            )

            url = self.tg_base_url + "editMessageMedia"
            data = data_obj.dict(exclude_none=True)

            r = await self._perform_async_request(url, data)
            return r
        
        media_obj = InputMedia(
            type=media_type,
            media="attach://media",
            caption=caption
        )
        data_obj = EditMessageMediaModel(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            media=media_obj,
            reply_markup=reply_markup
        )

        url = self.tg_base_url + "editMessageMedia"
        data = data_obj.dict(exclude_none=True)
        files = {"media": media}

        r = await self._perform_async_request(url, data, files=files)
        return r


    def sync_send_photo(
        self,
        chat_id: int,
        photo: Union[str, IO],
        caption: Optional[str] = None,
        parse_mode: str = "HTML",
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None
    ):
        if type(photo) == str:
            if photo.startswith("http://") or photo.startswith("https://"):
                photo_obj = Photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode=parse_mode,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    reply_to_message_id=reply_to_message_id,
                    allow_sending_without_reply=allow_sending_without_reply,
                    reply_markup=reply_markup
                )

                url = self.tg_base_url + "sendPhoto"
                data = photo_obj.dict(exclude_none=True)
                
                r = self._perform_sync_request(url, data)
                return r
            
            ends = [".jpg", ".jpeg", ".gif", ".png"]
            for end in ends:
                if photo.endswith(end):
                    opened_photo = open(photo, "rb")
                    photo_obj = Photo(
                        chat_id=chat_id,
                        photo=f"attach://{photo}",
                        caption=caption,
                        parse_mode=parse_mode,
                        disable_notification=disable_notification,
                        protect_content=protect_content,
                        reply_to_message_id=reply_to_message_id,
                        allow_sending_without_reply=allow_sending_without_reply,
                        reply_markup=reply_markup
                    )

                    url = self.tg_base_url + "sendPhoto"
                    data = photo_obj.dict(exclude_none=True)
                    data["reply_markup"] = json.dumps(data["reply_markup"])
                    files = {photo: opened_photo}
                    
                    r = self._perform_sync_request(url, data, use_json=False, files=files)
                    return r
            
            photo_obj = Photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup
            )

            url = self.tg_base_url + "sendPhoto"
            data = photo_obj.dict(exclude_none=True)
            
            r = self._perform_sync_request(url, data)
            return r
        
        photo_obj = Photo(
            chat_id=chat_id,
            photo="attach://image",
            caption=caption,
            parse_mode=parse_mode,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

        url = self.tg_base_url + "sendPhoto"
        data = photo_obj.dict(exclude_none=True)
        data["reply_markup"] = json.dumps(data["reply_markup"])
        files = {"image": photo}
        
        r = self._perform_sync_request(url, data, use_json=False, files=files)
        return r

    async def async_send_photo(
        self,
        chat_id: int,
        photo: Union[str, IO],
        caption: Optional[str] = None,
        parse_mode: str = "HTML",
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None
    ):
        if type(photo) == str:
            if photo.startswith("http://") or photo.startswith("https://"):
                photo_obj = Photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode=parse_mode,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    reply_to_message_id=reply_to_message_id,
                    allow_sending_without_reply=allow_sending_without_reply,
                    reply_markup=reply_markup
                )

                url = self.tg_base_url + "sendPhoto"
                data = photo_obj.dict(exclude_none=True)
                r = await self._perform_async_request(url, data)
                return r
            
            ends = [".jpg", ".jpeg", ".gif", ".png"]
            for end in ends:
                if photo.endswith(end):
                    async with aiofiles.open(photo, "rb") as opened_photo:
                        content = await opened_photo.read()
                    photo_obj = Photo(
                        chat_id=chat_id,
                        photo=f"attach://{photo}",
                        caption=caption,
                        parse_mode=parse_mode,
                        disable_notification=disable_notification,
                        protect_content=protect_content,
                        reply_to_message_id=reply_to_message_id,
                        allow_sending_without_reply=allow_sending_without_reply,
                        reply_markup=reply_markup
                    )

                    url = self.tg_base_url + "sendPhoto"
                    data = photo_obj.dict(exclude_none=True)
                    data["reply_markup"] = json.dumps(data["reply_markup"])
                    files = {photo: content}
                    r = await self._perform_async_request(url, data, use_json=False, files=files)
                    return r
            
            photo_obj = Photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup
            )

            url = self.tg_base_url + "sendPhoto"
            data = photo_obj.dict(exclude_none=True)
            r = await self._perform_async_request(url, data)
            return r
        
        photo_obj = Photo(
            chat_id=chat_id,
            photo="attach://image",
            caption=caption,
            parse_mode=parse_mode,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )

        url = self.tg_base_url + "sendPhoto"
        data = photo_obj.dict(exclude_none=True)
        data["reply_markup"] = json.dumps(data["reply_markup"])
        files = {"image": photo}
        r = await self._perform_async_request(url, data, use_json=False, files=files)
        return r


    @retry(
        retry=retry_if_exception_type(httpx.HTTPError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def sync_get_file(self, file_id: str):

        url = self.tg_base_url + "getFile"
        data = {
            "file_id": file_id
        }
        r = self._perform_sync_request(url, data)

        file_path = r["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        
        io_object = BytesIO()
        with httpx.stream(method="GET", url=download_url) as result:
            for data in result.iter_bytes():
                io_object.write(data)
        io_object.seek(0)

        return io_object

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError),
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def async_get_file(self, file_id: str):

        url = self.tg_base_url + "getFile"
        data = {
            "file_id": file_id
        }
        r = await self._perform_async_request(url, data)

        file_path = r["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        client = httpx.AsyncClient()

        io_object = BytesIO()
        async with client.stream(method="GET", url=download_url) as result:
            async for data in result.aiter_bytes():
                io_object.write(data)
        io_object.seek(0)

        return io_object

    def sync_send_media_group(
        self,
        chat_id: int,
        photos: Union[List[str], List[IO]]
    ):
        files = {}
        photos_list = []

        if type(photos[-1]) == str:
            if photos[-1].startswith("http://") or photos[-1].startswith("https://"):
                for photo in photos:
                    photos_list.append(
                        InputMediaPhoto(media=photo)
                    )
                
                media_group = MediaGroup(
                    chat_id=chat_id,
                    media=photos_list
                )
                url = self.tg_base_url + "sendMediaGroup"
                data = media_group.dict(exclude_none=True)
                r = self._perform_sync_request(url, data)
                return r
            
            ends = [".jpg", ".jpeg", ".gif", ".png"]
            for end in ends:
                if photos[-1].endswith(end):
                    for photo in photos:
                        photos_list.append(
                            InputMediaPhoto(media=f"attach://{photo}")
                        )
                        content = open(photo, "rb")
                        files[photo] = content
                    
                    media_group = MediaGroup(
                        chat_id=chat_id,
                        media=photos_list
                    )
                    url = self.tg_base_url + "sendMediaGroup"
                    data = media_group.dict(exclude_none=True)
                    data["media"] = json.dumps(data["media"])
                    r = self._perform_sync_request(url, data, use_json=False, files=files)
                    return r

            for photo in photos:
                photos_list.append(
                    InputMediaPhoto(media=photo)
                )
            
            media_group = MediaGroup(
                chat_id=chat_id,
                media=photos_list
            )
            url = self.tg_base_url + "sendMediaGroup"
            data = media_group.dict(exclude_none=True)
            r = self._perform_sync_request(url, data)
            return r

        for i in range(len(photos)):
            photos_list.append(
                InputMediaPhoto(media=f"attach://image_{i}")
            )
            files[f"image_{i}"] = photos[i]
        
        media_group = MediaGroup(
            chat_id=chat_id,
            media=photos_list
        )
        url = self.tg_base_url + "sendMediaGroup"
        data = media_group.dict(exclude_none=True)
        data["media"] = json.dumps(data["media"])
        r = self._perform_sync_request(url, data, use_json=False, files=files)
        return r

    async def async_send_media_group(
        self,
        chat_id: int,
        photos: Union[List[str], List[IO]]
    ):
        files = {}
        photos_list = []

        if type(photos[-1]) == str:
            if photos[-1].startswith("http://") or photos[-1].startswith("https://"):
                for photo in photos:
                    photos_list.append(
                        InputMediaPhoto(media=photo)
                    )
                
                media_group = MediaGroup(
                    chat_id=chat_id,
                    media=photos_list
                )
                url = self.tg_base_url + "sendMediaGroup"
                data = media_group.dict(exclude_none=True)
                r = await self._perform_async_request(url, data)
                return r
            
            ends = [".jpg", ".jpeg", ".gif", ".png"]
            for end in ends:
                if photos[-1].endswith(end):
                    for photo in photos:
                        photos_list.append(
                            InputMediaPhoto(media=f"attach://{photo}")
                        )
                        async with aiofiles.open(photo, "rb") as opened_photo:
                            content = await opened_photo.read()
                        files[photo] = content
                    
                    media_group = MediaGroup(
                        chat_id=chat_id,
                        media=photos_list
                    )
                    url = self.tg_base_url + "sendMediaGroup"
                    data = media_group.dict(exclude_none=True)
                    data["media"] = json.dumps(data["media"])
                    r = await self._perform_async_request(url, data, use_json=False, files=files)
                    return r

            for photo in photos:
                photos_list.append(
                    InputMediaPhoto(media=photo)
                )
            
            media_group = MediaGroup(
                chat_id=chat_id,
                media=photos_list
            )
            url = self.tg_base_url + "sendMediaGroup"
            data = media_group.dict(exclude_none=True)
            r = await self._perform_async_request(url, data)
            return r

        for i in range(len(photos)):
            photos_list.append(
                InputMediaPhoto(media=f"attach://image_{i}")
            )
            files[f"image_{i}"] = photos[i]
        
        media_group = MediaGroup(
            chat_id=chat_id,
            media=photos_list
        )
        url = self.tg_base_url + "sendMediaGroup"
        data = media_group.dict(exclude_none=True)
        data["media"] = json.dumps(data["media"])
        r = await self._perform_async_request(url, data, use_json=False, files=files)
        return r
