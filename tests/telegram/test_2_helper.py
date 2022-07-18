import httpx
import pytest
from pytest_httpx import HTTPXMock

from multibotkit.helpers.telegram import TelegramHelper
from multibotkit.schemas.telegram.outgoing import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebhookInfo,
)
from tests.config import settings


tg_helper = TelegramHelper(settings.TG_TOKEN)


def test_sync_helper_get_webhook_info(httpx_mock: HTTPXMock):
    def webhook_info_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "ok": True,
                "result": {
                    "url": "https://test_url/api/bot/telegram",
                    "has_custom_certificate": False,
                    "pending_update_count": 2,
                    "ip_address": "111.111.111.111",
                    "last_error_date": 1656425873,
                    "last_error_message": "error message",
                    "max_connections": 10,
                    "allowed_updates": [
                        "message",
                        "edited_channel_post",
                        "callback_query",
                    ],
                },
            },
        )

    httpx_mock.add_callback(webhook_info_response)

    r = tg_helper.syncGetWebhookInfo()

    assert r == WebhookInfo.parse_obj(
        {
            "url": "https://test_url/api/bot/telegram",
            "has_custom_certificate": False,
            "pending_update_count": 2,
            "ip_address": "111.111.111.111",
            "last_error_date": 1656425873,
            "last_error_message": "error message",
            "max_connections": 10,
            "allowed_updates": ["message", "edited_channel_post", "callback_query"],
        }
    )


def test_sync_helper_set_webhook(httpx_mock: HTTPXMock):
    def set_webhook_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"ok": True, "result": True, "description": "Webhook was set"},
        )

    httpx_mock.add_callback(set_webhook_response)

    r = tg_helper.syncSetWebhook(webhook_url="https://test_url/api/bot")

    assert r == {"ok": True, "result": True, "description": "Webhook was set"}


def test_sync_helper_answer_callback_query(httpx_mock: HTTPXMock):
    def answer_callback_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(answer_callback_response)

    r = tg_helper.syncAnswerCallbackQuery(callback_query_id="callback_query_id")

    assert r == {"ok": True, "result": True}


def test_sync_helper_edit_message_text(httpx_mock: HTTPXMock):
    def edit_message_text_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_text_response)

    r = tg_helper.syncEditMessageText(chat_id=1234, message_id=1111, text="new text")

    assert r == {"ok": True, "result": True}


def test_sync_helper_edit_message_caption(httpx_mock: HTTPXMock):
    def edit_message_caption_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_caption_response)

    r = tg_helper.syncEditMessageCaption(
        chat_id=1234, message_id=1111, caption="New caption"
    )

    assert r == {"ok": True, "result": True}


def test_sync_helper_edit_message_reply_markup(httpx_mock: HTTPXMock):
    def edit_message_reply_markup_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_reply_markup_response)

    keyboard_button = KeyboardButton(
        text="Button", request_contact=False, request_location=False
    )

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False,
    )

    r = tg_helper.syncEditMessageReplyMarkup(
        chat_id=1234, message_id=1111, reply_markup=reply_keyboard_markup
    )

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_async_get_webhook_info(httpx_mock: HTTPXMock):
    def webhook_info_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "ok": True,
                "result": {
                    "url": "https://test_url/api/bot/telegram",
                    "has_custom_certificate": False,
                    "pending_update_count": 2,
                    "ip_address": "111.111.111.111",
                    "last_error_date": 1656425873,
                    "last_error_message": "error message",
                    "max_connections": 10,
                    "allowed_updates": [
                        "message",
                        "edited_channel_post",
                        "callback_query",
                    ],
                },
            },
        )

    httpx_mock.add_callback(webhook_info_response)

    r = await tg_helper.asyncGetWebhookInfo()

    assert r == WebhookInfo.parse_obj(
        {
            "url": "https://test_url/api/bot/telegram",
            "has_custom_certificate": False,
            "pending_update_count": 2,
            "ip_address": "111.111.111.111",
            "last_error_date": 1656425873,
            "last_error_message": "error message",
            "max_connections": 10,
            "allowed_updates": ["message", "edited_channel_post", "callback_query"],
        }
    )


@pytest.mark.asyncio
async def test_async_helper_async_set_webhook(httpx_mock: HTTPXMock):
    def set_webhook_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"ok": True, "result": True, "description": "Webhook was set"},
        )

    httpx_mock.add_callback(set_webhook_response)

    r = await tg_helper.asyncSetWebhook(webhook_url="https://test_url/api/bot")

    assert r == {"ok": True, "result": True, "description": "Webhook was set"}


@pytest.mark.asyncio
async def test_async_helper_answer_callback_query(httpx_mock: HTTPXMock):
    def answer_callback_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(answer_callback_response)

    r = await tg_helper.asyncAnswerCallbackQuery(callback_query_id="callback_query_id")

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_edit_message_text(httpx_mock: HTTPXMock):
    def edit_message_text_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_text_response)

    r = await tg_helper.asyncEditMessageText(
        chat_id=1234, message_id=1111, text="new text"
    )

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_edit_message_caption(httpx_mock: HTTPXMock):
    def edit_message_caption_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_caption_response)

    r = await tg_helper.asyncEditMessageCaption(
        chat_id=1234, message_id=1111, caption="New caption"
    )

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_edit_message_reply_markup(httpx_mock: HTTPXMock):
    def edit_message_reply_markup_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_reply_markup_response)

    keyboard_button = KeyboardButton(
        text="Button", request_contact=False, request_location=False
    )

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False,
    )

    r = await tg_helper.asyncEditMessageReplyMarkup(
        chat_id=1234, message_id=1111, reply_markup=reply_keyboard_markup
    )

    assert r == {"ok": True, "result": True}
