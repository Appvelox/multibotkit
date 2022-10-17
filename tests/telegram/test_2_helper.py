import io
from tempfile import NamedTemporaryFile
import httpx
import json
import pytest
from pytest_httpx import HTTPXMock, IteratorStream

from multibotkit.helpers.telegram import TelegramHelper
from multibotkit.schemas.telegram.outgoing import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
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

    r = tg_helper.sync_get_webhook_info()

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

    r = tg_helper.sync_set_webhook(webhook_url="https://test_url/api/bot")

    assert r == {"ok": True, "result": True, "description": "Webhook was set"}


def test_sync_send_message(httpx_mock: HTTPXMock):
    def send_message_response(request: httpx.Request):
        content = json.loads(request.content.decode())

        return httpx.Response(
            status_code=200, json={"ok": True, "result": True, "message": content}
        )

    httpx_mock.add_callback(send_message_response)

    keyboard_button_dict = {
        "text": "Button",
        "request_contact": False,
        "request_location": False,
    }

    keyboard_button = KeyboardButton.parse_obj(keyboard_button_dict)

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False,
    )

    message = Message(
        chat_id=1234,
        text="text",
        disable_web_page_preview=False,
        reply_markup=reply_keyboard_markup,
    )

    message_dict = message.dict(exclude_none=True)
    message_dict.update({"parse_mode": "HTML"})

    r = tg_helper.sync_send_message(
        chat_id=1234,
        text="text",
        disable_web_page_preview=False,
        reply_markup=reply_keyboard_markup,
    )

    assert r == {"ok": True, "result": True, "message": message_dict}


def test_sync_helper_answer_callback_query(httpx_mock: HTTPXMock):
    def answer_callback_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(answer_callback_response)

    r = tg_helper.sync_answer_callback_query(callback_query_id="callback_query_id")

    assert r == {"ok": True, "result": True}


def test_sync_helper_edit_message_text(httpx_mock: HTTPXMock):
    def edit_message_text_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_text_response)

    r = tg_helper.sync_edit_message_text(chat_id=1234, message_id=1111, text="new text")

    assert r == {"ok": True, "result": True}


def test_sync_helper_edit_message_caption(httpx_mock: HTTPXMock):
    def edit_message_caption_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_caption_response)

    r = tg_helper.sync_edit_message_caption(
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

    r = tg_helper.sync_edit_message_reply_markup(
        chat_id=1234, message_id=1111, reply_markup=reply_keyboard_markup
    )

    assert r == {"ok": True, "result": True}


def test_sync_helper_edit_message_media(httpx_mock: HTTPXMock):
    def edit_media_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_media_response)
    httpx_mock.add_callback(edit_media_response)

    keyboard_button_dict = {
        "text": "Button",
        "callback_data": "some_data"
    }

    keyboard_button = InlineKeyboardButton.parse_obj(keyboard_button_dict)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[keyboard_button, keyboard_button]],
    )

    r = tg_helper.sync_edit_message_media(
        media="file_id",
        media_type="photo",
        caption="caption",
        chat_id=1234,
        message_id=120,
        reply_markup=keyboard
    )

    assert r == {"ok": True, "result": True}

    photo = io.BytesIO()

    r = tg_helper.sync_edit_message_media(
        media=photo,
        media_type="photo",
        caption="caption",
        chat_id=1234,
        message_id=120,
        reply_markup=keyboard
    )

    assert r == {"ok": True, "result": True}


def test_sync_helper_send_photo(httpx_mock: HTTPXMock):
    def send_photo_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(send_photo_response)
    httpx_mock.add_callback(send_photo_response)

    keyboard_button_dict = {
        "text": "Button",
        "request_contact": False,
        "request_location": False,
    }

    keyboard_button = KeyboardButton.parse_obj(keyboard_button_dict)

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False,
    )

    r = tg_helper.sync_send_photo(
        chat_id=1234,
        photo="file_id",
        reply_markup=reply_keyboard_markup
    )

    assert r == {"ok": True, "result": True}

    r = tg_helper.sync_send_photo(
        chat_id=1234,
        photo="file_id",
    )

    assert r == {"ok": True, "result": True}

    photo = NamedTemporaryFile()

    r = tg_helper.sync_send_photo(
        chat_id=1234,
        photo=photo,
        reply_markup=reply_keyboard_markup
    )

    assert r == {"ok": True, "result": True}

    r = tg_helper.sync_send_photo(
        chat_id=1234,
        photo=photo,
    )

    assert r == {"ok": True, "result": True}


def test_sync_helper_get_file(httpx_mock: HTTPXMock):
    def get_file_path_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"ok": True, "result": {"file_path": "file_path"}}
        )
    
    httpx_mock.add_callback(get_file_path_response)
    httpx_mock.add_response(stream=IteratorStream([b"part 1", b"part 2"]))

    doc = tg_helper.sync_get_file(file_id="file_id")
    assert doc.readline() == b"part 1part 2"


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

    r = await tg_helper.async_get_webhook_info()

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

    r = await tg_helper.async_set_webhook(webhook_url="https://test_url/api/bot")

    assert r == {"ok": True, "result": True, "description": "Webhook was set"}


@pytest.mark.asyncio
async def test_async_send_message(httpx_mock: HTTPXMock):
    def send_message_response(request: httpx.Request):
        content = json.loads(request.content.decode())

        return httpx.Response(
            status_code=200, json={"ok": True, "result": True, "message": content}
        )

    httpx_mock.add_callback(send_message_response)

    keyboard_button_dict = {
        "text": "Button",
        "request_contact": False,
        "request_location": False,
    }

    keyboard_button = KeyboardButton.parse_obj(keyboard_button_dict)

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False,
    )

    message = Message(
        chat_id=1234,
        text="text",
        disable_web_page_preview=False,
        reply_markup=reply_keyboard_markup,
    )

    message_dict = message.dict(exclude_none=True)
    message_dict.update({"parse_mode": "HTML"})

    r = await tg_helper.async_send_message(
        chat_id=1234,
        text="text",
        disable_web_page_preview=False,
        reply_markup=reply_keyboard_markup,
    )

    assert r == {"ok": True, "result": True, "message": message_dict}


@pytest.mark.asyncio
async def test_async_helper_answer_callback_query(httpx_mock: HTTPXMock):
    def answer_callback_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(answer_callback_response)

    r = await tg_helper.async_answer_callback_query(
        callback_query_id="callback_query_id"
    )

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_edit_message_text(httpx_mock: HTTPXMock):
    def edit_message_text_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_text_response)

    r = await tg_helper.async_edit_message_text(
        chat_id=1234, message_id=1111, text="new text"
    )

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_edit_message_caption(httpx_mock: HTTPXMock):
    def edit_message_caption_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_message_caption_response)

    r = await tg_helper.async_edit_message_caption(
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

    r = await tg_helper.async_edit_message_reply_markup(
        chat_id=1234, message_id=1111, reply_markup=reply_keyboard_markup
    )

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_edit_message_media(httpx_mock: HTTPXMock):
    def edit_media_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(edit_media_response)
    httpx_mock.add_callback(edit_media_response)

    keyboard_button_dict = {
        "text": "Button",
        "callback_data": "some_data"
    }

    keyboard_button = InlineKeyboardButton.parse_obj(keyboard_button_dict)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[keyboard_button, keyboard_button]],
    )

    r = await tg_helper.async_edit_message_media(
        media="file_id",
        media_type="photo",
        caption="caption",
        chat_id=1234,
        message_id=120,
        reply_markup=keyboard
    )

    assert r == {"ok": True, "result": True}

    photo = io.BytesIO()

    r = await tg_helper.async_edit_message_media(
        media=photo,
        media_type="photo",
        caption="caption",
        chat_id=1234,
        message_id=120,
        reply_markup=keyboard
    )

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_send_photo(httpx_mock: HTTPXMock):
    def send_photo_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "result": True})

    httpx_mock.add_callback(send_photo_response)
    httpx_mock.add_callback(send_photo_response)

    keyboard_button_dict = {
        "text": "Button",
        "request_contact": False,
        "request_location": False,
    }

    keyboard_button = KeyboardButton.parse_obj(keyboard_button_dict)

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False,
    )

    r = await tg_helper.async_send_photo(
        chat_id=1234,
        photo="file_id",
        reply_markup=reply_keyboard_markup
    )

    assert r == {"ok": True, "result": True}

    r = await tg_helper.async_send_photo(
        chat_id=1234,
        photo="file_id",
    )

    assert r == {"ok": True, "result": True}

    photo = NamedTemporaryFile()

    r = await tg_helper.async_send_photo(
        chat_id=1234,
        photo=photo,
        reply_markup=reply_keyboard_markup
    )

    assert r == {"ok": True, "result": True}

    r = await tg_helper.async_send_photo(
        chat_id=1234,
        photo=photo,
    )

    assert r == {"ok": True, "result": True}


@pytest.mark.asyncio
async def test_async_helper_get_file(httpx_mock: HTTPXMock):
    def get_file_path_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"ok": True, "result": {"file_path": "file_path"}}
        )
    
    httpx_mock.add_callback(get_file_path_response)
    httpx_mock.add_response(stream=IteratorStream([b"part 1", b"part 2"]))

    doc = await tg_helper.async_get_file(file_id="file_id")
    assert doc.readline() == b"part 1part 2"
