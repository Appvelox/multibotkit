from xml import dom
import httpx
import logging
from typing import Optional

from multibotkit.schemas.telegram.outgoing import (
    InlineKeyboardMarkup,
    Message,
    SetWebhookParams, 
    WebhookInfo
)


logger = logging.getLogger('events')


class TelegramHelper:
    """
    Sync and async functions for Telegram Bot API
    """
    def __init__(self, token):
        self.token = token
        self.tg_base_url = f"https://api.telegram.org/bot{self.token}/"
    

    def getWebhookInfo(self) -> Optional[WebhookInfo]:
        url = self.tg_base_url + "getWebhookInfo"
        r = httpx.post(url)
        data = r.json()
        if data["ok"] is True:
            return WebhookInfo(**data["result"])
        return None

    async def async_getWebhookInfo(self) -> Optional[WebhookInfo]:
        url = self.tg_base_url + "getWebhookInfo"
        async with httpx.AsyncClient() as client:
            r = await client.post(url)
        data = r.json()
        if data["ok"] is True:
            return WebhookInfo(**data["result"])
        return None


    def setWebhook(self, domain):
        url = self.tg_base_url + "setWebhook"
        webhook_url = f"https://{domain}/api/bot/telegram"
        params = SetWebhookParams(url=webhook_url)
        data = params.dict(exclude_none=True)
        r = httpx.post(url, data=data)
        return r

    async def async_setWebhook(self, domain):
        url = self.tg_base_url + "setWebhook"
        webhook_url = f"https://{domain}/api/bot/telegram"
        params = SetWebhookParams(url=webhook_url)
        data = params.dict(exclude_none=True)
        async with httpx.AsyncClient() as client:
            r = await client.post(url, data=data)
            return r


    def set_tg_webhook(self, domain: str):
        logger.info("Checking current telegram webhook configuration")
        wb_info = self.getWebhookInfo()
        if wb_info is None or wb_info.url != f"https://{domain}/api/bot/telegram":
            logger.info("Telegram webhook configuration mismatch. Updating configuration.")
            r = self.setWebhook(domain=domain)
            return r

    async def async_set_tg_webhook(self, domain: str):
        logger.info("Checking current telegram webhook configuration")
        wb_info = await self.async_getWebhookInfo()
        if wb_info is None or wb_info.url != f"https://{domain}/api/bot/telegram":
            logger.info("Telegram webhook configuration mismatch. Updating configuration.")
            r = await self.async_setWebhook(domain=domain)
            return r


    def send_message(self, message: Message):
        url = self.tg_base_url + "sendMessage"
        data = message.dict(exclude_none=True)
        data.update({"parse_mode": "HTML"})
        r = httpx.post(url, json=data)
        return r

    async def async_send_message(self, message: Message):
        url = self.tg_base_url + "sendMessage"
        data = message.dict(exclude_none=True)
        data.update({"parse_mode": "HTML"})
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=data)
            return r


    def answer_callback_query(self, callback_query_id: str):
        url = self.tg_base_url + "answerCallbackQuery"
        data = {"callback_query_id": callback_query_id}
        r = httpx.post(url, json=data)
        return r
    
    async def async_answer_callback_query(self, callback_query_id: str):
        url = self.tg_base_url + "answerCallbackQuery"
        data = {"callback_query_id": callback_query_id}
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=data)
            return r


    def edit_message_text(self, chat_id: int, message_id: int, text: str):
        url = self.tg_base_url + "editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        r = httpx.post(url, json=data)
        return r

    async def async_edit_message_text(self, chat_id: int, message_id: int, text: str):
        url = self.tg_base_url + "editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=data)
            return r


    def edit_message_caption(self, chat_id: int, message_id: int, caption: str):
        url = self.tg_base_url + "editMessageCaption"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": "Markdown",
        }
        r = httpx.post(url, json=data)
        return r
    
    async def async_edit_message_caption(self, chat_id: int, message_id: int, caption: str):
        url = self.tg_base_url + "editMessageCaption"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": "Markdown",
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=data)
            return r


    def edit_message_reply_markup(
        self, chat_id: int, message_id:int, reply_markup: Optional[InlineKeyboardMarkup]
    ):
        url = self.tg_base_url + "editMessageReplyMarkup"
        try:
            data = {
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": reply_markup.dict(exclude_none=True),
            }
        except AttributeError:
            data = {
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": {},
            }
        r = httpx.post(url, json=data)
        return r


    async def async_edit_message_reply_markup(
        self, chat_id: int, message_id:int, reply_markup: Optional[InlineKeyboardMarkup]
    ):
        url = self.tg_base_url + "editMessageReplyMarkup"
        try:
            data = {
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": reply_markup.dict(exclude_none=True),
            }
        except AttributeError:
            data = {
                "chat_id": chat_id,
                "message_id": message_id,
                "reply_markup": {},
            }
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=data)
            return r
