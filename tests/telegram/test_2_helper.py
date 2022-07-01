import httpx
import pytest
from pytest_httpx import HTTPXMock

from multibotkit.helpers.telegram import TelegramHelper
from multibotkit.schemas.telegram.outgoing import ReplyKeyboardMarkup, KeyboardButton, WebhookInfo
from tests.config import settings


tg_helper = TelegramHelper(settings.TG_TOKEN)


def test_helper_get_webhook_info(httpx_mock: HTTPXMock):
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
                    "allowed_updates": ["message", "edited_channel_post", "callback_query"]
                }
            }
        )

    httpx_mock.add_callback(webhook_info_response)

    r = tg_helper.getWebhookInfo()
    
    assert r == WebhookInfo.parse_obj({
                "url": "https://test_url/api/bot/telegram",
                "has_custom_certificate": False,
                "pending_update_count": 2,
                "ip_address": "111.111.111.111",
                "last_error_date": 1656425873,
                "last_error_message": "error message",
                "max_connections": 10,
                "allowed_updates": ["message", "edited_channel_post", "callback_query"]
            })


def test_helper_set_webhook(httpx_mock: HTTPXMock):
    def set_webhook_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True, 
                'description': 'Webhook was set'
            }
        )
    
    httpx_mock.add_callback(set_webhook_response)

    r = tg_helper.setWebhook(domain="test_url")

    assert r.json() == {
        'ok': True, 
                'result': True, 
                'description': 'Webhook was set'
    }


def test_helper_set_tg_webhook(httpx_mock: HTTPXMock):
    def webhook_info_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "ok": True,
                "result": {
                    "url": "https://another_test_url/api/bot/telegram",
                    "has_custom_certificate": False,
                    "pending_update_count": 2,
                    "ip_address": "111.111.111.111",
                    "last_error_date": 1656425873,
                    "last_error_message": "error message",
                    "max_connections": 10,
                    "allowed_updates": ["message", "edited_channel_post", "callback_query"]
                }
            }
        )
    
    def set_tg_webhook_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True, 
                'description': 'Webhook was set'
            }
        )
    
    httpx_mock.add_callback(webhook_info_response)
    httpx_mock.add_callback(set_tg_webhook_response)

    r = tg_helper.set_tg_webhook(domain="test_url")

    assert r.json() == {
        'ok': True, 
        'result': True, 
        'description': 'Webhook was set'
    }


def test_helper_answer_callback_query(httpx_mock: HTTPXMock):
    def answer_callback_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True
            }
        )
    
    httpx_mock.add_callback(answer_callback_response)

    r = tg_helper.answer_callback_query(callback_query_id="callback_query_id")

    assert r.json() == {
                'ok': True, 
                'result': True
            }


def test_helper_edit_message_text(httpx_mock: HTTPXMock):
    def edit_message_text_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True
            }
        )

    httpx_mock.add_callback(edit_message_text_response)

    r = tg_helper.edit_message_text(chat_id=1234, message_id=1111, text="new text")

    assert r.json() == {
                'ok': True, 
                'result': True
            }


def test_helper_edit_message_caption(httpx_mock: HTTPXMock):
    def edit_message_caption_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True
            }
        )

    httpx_mock.add_callback(edit_message_caption_response)

    r = tg_helper.edit_message_caption(chat_id=1234, message_id=1111, caption="New caption")

    assert r.json() == {
                'ok': True, 
                'result': True
            }


def test_helper_edit_message_reply_markup(httpx_mock: HTTPXMock):
    def edit_message_reply_markup_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True
            }
        )

    httpx_mock.add_callback(edit_message_reply_markup_response)

    keyboard_button = KeyboardButton(
        text="Button",
        request_contact=False,
        request_location=False
    )

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False
    )

    r = tg_helper.edit_message_reply_markup(chat_id=1234, message_id=1111, reply_markup=reply_keyboard_markup)

    assert r.json() == {
                'ok': True, 
                'result': True
            }


@pytest.mark.asyncio
async def test_helper_async_get_webhook_info(httpx_mock: HTTPXMock):
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
                    "allowed_updates": ["message", "edited_channel_post", "callback_query"]
                }
            }
        )

    httpx_mock.add_callback(webhook_info_response)

    r = await tg_helper.async_getWebhookInfo()
    
    assert r == WebhookInfo.parse_obj({
                "url": "https://test_url/api/bot/telegram",
                "has_custom_certificate": False,
                "pending_update_count": 2,
                "ip_address": "111.111.111.111",
                "last_error_date": 1656425873,
                "last_error_message": "error message",
                "max_connections": 10,
                "allowed_updates": ["message", "edited_channel_post", "callback_query"]
            })


@pytest.mark.asyncio
async def test_helper_async_set_webhook(httpx_mock: HTTPXMock):
    def set_webhook_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True, 
                'description': 'Webhook was set'
            }
        )
    
    httpx_mock.add_callback(set_webhook_response)

    r = await tg_helper.async_setWebhook(domain="test_url")

    assert r.json() == {
        'ok': True, 
        'result': True, 
        'description': 'Webhook was set'
    }


@pytest.mark.asyncio
async def test_helper_async_set_tg_webhook(httpx_mock: HTTPXMock):
    def webhook_info_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "ok": True,
                "result": {
                    "url": "https://another_test_url/api/bot/telegram",
                    "has_custom_certificate": False,
                    "pending_update_count": 2,
                    "ip_address": "111.111.111.111",
                    "last_error_date": 1656425873,
                    "last_error_message": "error message",
                    "max_connections": 10,
                    "allowed_updates": ["message", "edited_channel_post", "callback_query"]
                }
            }
        )
    
    def set_tg_webhook_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True, 
                'description': 'Webhook was set'
            }
        )
    
    httpx_mock.add_callback(webhook_info_response)
    httpx_mock.add_callback(set_tg_webhook_response)

    r = await tg_helper.async_set_tg_webhook(domain="test_url")

    assert r.json() == {
        'ok': True, 
        'result': True, 
        'description': 'Webhook was set'
    }


@pytest.mark.asyncio
async def test_helper_answer_callback_query(httpx_mock: HTTPXMock):
    def answer_callback_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True
            }
        )
    
    httpx_mock.add_callback(answer_callback_response)

    r = await tg_helper.async_answer_callback_query(callback_query_id="callback_query_id")

    assert r.json() == {
                'ok': True, 
                'result': True
            }


@pytest.mark.asyncio
async def test_helper_edit_message_text(httpx_mock: HTTPXMock):
    def edit_message_text_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True
            }
        )

    httpx_mock.add_callback(edit_message_text_response)

    r = await tg_helper.async_edit_message_text(chat_id=1234, message_id=1111, text="new text")

    assert r.json() == {
                'ok': True, 
                'result': True
            }


@pytest.mark.asyncio
async def test_helper_edit_message_caption(httpx_mock: HTTPXMock):
    def edit_message_caption_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True
            }
        )

    httpx_mock.add_callback(edit_message_caption_response)

    r = await tg_helper.async_edit_message_caption(chat_id=1234, message_id=1111, caption="New caption")

    assert r.json() == {
                'ok': True, 
                'result': True
            }


@pytest.mark.asyncio
async def test_helper_edit_message_reply_markup(httpx_mock: HTTPXMock):
    def edit_message_reply_markup_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                'ok': True, 
                'result': True
            }
        )

    httpx_mock.add_callback(edit_message_reply_markup_response)

    keyboard_button = KeyboardButton(
        text="Button",
        request_contact=False,
        request_location=False
    )

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False
    )

    r = await tg_helper.async_edit_message_reply_markup(chat_id=1234, message_id=1111, reply_markup=reply_keyboard_markup)

    assert r.json() == {
                'ok': True, 
                'result': True
            }