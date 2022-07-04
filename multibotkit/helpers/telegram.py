from xml import dom
import httpx
import logging
import sentry_sdk
from tenacity import retry
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


    @retry
    def _perform_sync_request(self, url:str, data:dict=None):
        try:
            r = httpx.post(url=url, json=data)
            return r
        except Exception as ex:
            sentry_sdk.capture_exception()

    @retry
    async def _perform_async_request(self, url:str, data:dict=None):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(url, data=data)
                return r
        except Exception as ex:
            sentry_sdk.capture_exception()


    @retry
    def syncGetWebhookInfo(self) -> Optional[WebhookInfo]:
        url = self.tg_base_url + "getWebhookInfo"
        r = self._perform_sync_request(url)
        try:
            data = r.json()
            if data["ok"] is True:
                return WebhookInfo(**data["result"])
            return None
        except Exception as ex:
            sentry_sdk.capture_exception()

    @retry
    async def asyncGetWebhookInfo(self) -> Optional[WebhookInfo]:
        url = self.tg_base_url + "getWebhookInfo"
        r = await self._perform_async_request(url)
        try:
            data = r.json()
            if data["ok"] is True:
                return WebhookInfo(**data["result"])
            return None
        except Exception as ex:
            sentry_sdk.capture_exception()


    @retry
    def syncSetWebhook(self, domain):
        url = self.tg_base_url + "setWebhook"
        webhook_url = f"https://{domain}/api/bot/telegram"
        params = SetWebhookParams(url=webhook_url)
        data = params.dict(exclude_none=True)
        r = self._perform_sync_request(url, data)
        return r

    @retry
    async def asyncSetWebhook(self, domain):
        url = self.tg_base_url + "setWebhook"
        webhook_url = f"https://{domain}/api/bot/telegram"
        params = SetWebhookParams(url=webhook_url)
        data = params.dict(exclude_none=True)
        r = await self._perform_async_request(url, data)
        return r


    @retry
    def syncSetTGWebhook(self, domain: str):
        logger.info("Checking current telegram webhook configuration")
        wb_info = self.syncGetWebhookInfo()
        if wb_info is None or wb_info.url != f"https://{domain}/api/bot/telegram":
            logger.info("Telegram webhook configuration mismatch. Updating configuration.")
            r = self.syncSetWebhook(domain=domain)
            return r

    @retry
    async def asyncSetTGWebhook(self, domain: str):
        logger.info("Checking current telegram webhook configuration")
        wb_info = await self.asyncGetWebhookInfo()
        if wb_info is None or wb_info.url != f"https://{domain}/api/bot/telegram":
            logger.info("Telegram webhook configuration mismatch. Updating configuration.")
            r = await self.asyncSetWebhook(domain=domain)
            return r


    @retry
    def syncSendMessage(self, message: Message):
        url = self.tg_base_url + "sendMessage"
        data = message.dict(exclude_none=True)
        data.update({"parse_mode": "HTML"})
        r = self._perform_sync_request(url, data)
        return r

    @retry
    async def asyncSendMessage(self, message: Message):
        url = self.tg_base_url + "sendMessage"
        data = message.dict(exclude_none=True)
        data.update({"parse_mode": "HTML"})
        r = await self._perform_async_request(url, data)
        return r


    @retry
    def syncAnswerCallbackQuery(self, callback_query_id: str):
        url = self.tg_base_url + "answerCallbackQuery"
        data = {"callback_query_id": callback_query_id}
        r = self._perform_sync_request(url, data)
        return r

    @retry
    async def asyncAnswerCallbackQuery(self, callback_query_id: str):
        url = self.tg_base_url + "answerCallbackQuery"
        data = {"callback_query_id": callback_query_id}
        r = await self._perform_async_request(url, data)
        return r


    @retry
    def syncEditMessageText(self, chat_id: int, message_id: int, text: str):
        url = self.tg_base_url + "editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        r = self._perform_sync_request(url, data)
        return r

    @retry
    async def asyncEditMessageText(self, chat_id: int, message_id: int, text: str):
        url = self.tg_base_url + "editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        r = await self._perform_async_request(url, data)
        return r


    @retry
    def syncEditMessageCaption(self, chat_id: int, message_id: int, caption: str):
        url = self.tg_base_url + "editMessageCaption"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": "Markdown",
        }
        r = self._perform_sync_request(url, data)
        return r
    
    @retry
    async def asyncEditMessageCaption(self, chat_id: int, message_id: int, caption: str):
        url = self.tg_base_url + "editMessageCaption"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": "Markdown",
        }
        r = await self._perform_async_request(url, data)
        return r


    @retry
    def syncEditMessageReplyMarkup(
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
        r = self._perform_sync_request(url, data)
        return r

    @retry
    async def asyncEditMessageReplyMarkup(
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
        r = await self._perform_async_request(url, data)
        return r
