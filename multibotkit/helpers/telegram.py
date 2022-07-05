from json import JSONDecodeError
import httpx
import logging
from tenacity import (
    retry, 
    retry_if_exception_type, 
    stop_after_attempt, 
    wait_exponential
)
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


    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)|retry_if_exception_type(JSONDecodeError), 
        reraise=True, 
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _perform_sync_request(self, url:str, data:dict=None):
        r = httpx.post(url=url, json=data)
        return r.json()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError)|retry_if_exception_type(JSONDecodeError),
        reraise=True, 
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _perform_async_request(self, url:str, data:dict=None):
        async with httpx.AsyncClient() as client:
            r = await client.post(url, data=data)
            return r.json()


    def syncGetWebhookInfo(self) -> Optional[WebhookInfo]:
        url = self.tg_base_url + "getWebhookInfo"
        r = self._perform_sync_request(url)
        if r["ok"] is True:
            return WebhookInfo(**r["result"])
        return None

    async def asyncGetWebhookInfo(self) -> Optional[WebhookInfo]:
        url = self.tg_base_url + "getWebhookInfo"
        r = await self._perform_async_request(url)
        if r["ok"] is True:
            return WebhookInfo(**r["result"])
        return None


    def syncSetWebhook(self, webhook_url: str):
        url = self.tg_base_url + "setWebhook"
        params = SetWebhookParams(url=webhook_url)
        data = params.dict(exclude_none=True)
        r = self._perform_sync_request(url, data)
        return r

    async def asyncSetWebhook(self, webhook_url: str):
        url = self.tg_base_url + "setWebhook"
        params = SetWebhookParams(url=webhook_url)
        data = params.dict(exclude_none=True)
        r = await self._perform_async_request(url, data)
        return r


    def syncSendMessage(self, message: Message, parse_mode: str="HTML"):
        url = self.tg_base_url + "sendMessage"
        data = message.dict(exclude_none=True)
        data.update({"parse_mode": parse_mode})
        r = self._perform_sync_request(url, data)
        return r

    async def asyncSendMessage(self, message: Message, parse_mode: str="HTML"):
        url = self.tg_base_url + "sendMessage"
        data = message.dict(exclude_none=True)
        data.update({"parse_mode": parse_mode})
        r = await self._perform_async_request(url, data)
        return r


    def syncAnswerCallbackQuery(self, callback_query_id: str):
        url = self.tg_base_url + "answerCallbackQuery"
        data = {"callback_query_id": callback_query_id}
        r = self._perform_sync_request(url, data)
        return r

    async def asyncAnswerCallbackQuery(self, callback_query_id: str):
        url = self.tg_base_url + "answerCallbackQuery"
        data = {"callback_query_id": callback_query_id}
        r = await self._perform_async_request(url, data)
        return r


    def syncEditMessageText(self, chat_id: int, message_id: int, text: str):
        url = self.tg_base_url + "editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        r = self._perform_sync_request(url, data)
        return r

    async def asyncEditMessageText(self, chat_id: int, message_id: int, text: str):
        url = self.tg_base_url + "editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        r = await self._perform_async_request(url, data)
        return r


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
