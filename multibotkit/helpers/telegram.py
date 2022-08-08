from typing import Optional, Union

from multibotkit.helpers.base_helper import BaseHelper
from multibotkit.schemas.telegram.outgoing import (
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
    SetWebhookParams,
    WebhookInfo,
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
