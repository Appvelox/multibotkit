import io
import json

import httpx
import pytest
from pytest_httpx import HTTPXMock

from multibotkit.helpers.yandexmessenger import YandexMessengerHelper
from multibotkit.schemas.yandexmessenger.outgoing import (
    InlineKeyboard,
    InlineKeyboardButton,
)
from tests.config import settings

ym_helper = YandexMessengerHelper(settings.YANDEX_MESSENGER_TOKEN)


@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
def test_sync_helper_send_text(httpx_mock: HTTPXMock):
    """Тест синхронной отправки текста"""

    def send_text_response(request: httpx.Request):
        # Проверка OAuth заголовка
        assert "Authorization" in request.headers
        assert request.headers["Authorization"].startswith("OAuth ")

        _ = json.loads(request.content.decode())

        return httpx.Response(status_code=200, json={"ok": True, "message_id": 12345})

    httpx_mock.add_callback(send_text_response)

    r = ym_helper.sync_send_text(text="Test message", login="test_user")

    assert r["ok"] is True
    assert r["message_id"] == 12345


@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
def test_sync_helper_send_text_with_keyboard(httpx_mock: HTTPXMock):
    """Тест отправки текста с inline клавиатурой"""

    def send_text_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "message_id": 12345})

    httpx_mock.add_callback(send_text_response)

    button1 = InlineKeyboardButton(text="Button 1", callback_data={"action": "1"})
    button2 = InlineKeyboardButton(text="Button 2", callback_data={"action": "2"})
    keyboard = InlineKeyboard(buttons=[button1, button2])

    r = ym_helper.sync_send_text(
        text="Choose option", chat_id="group_123", inline_keyboard=keyboard
    )

    assert r["ok"] is True
    assert r["message_id"] == 12345


@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
def test_sync_helper_send_image_io(httpx_mock: HTTPXMock):
    """Тест отправки изображения через IO объект"""

    def send_image_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "message_id": 12346})

    httpx_mock.add_callback(send_image_response)

    image_io = io.BytesIO(b"fake image data")

    r = ym_helper.sync_send_image(image=image_io, login="test_user")

    assert r["ok"] is True
    assert r["message_id"] == 12346


@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
def test_sync_helper_send_file(httpx_mock: HTTPXMock):
    """Тест отправки файла"""

    def send_file_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "message_id": 12347})

    httpx_mock.add_callback(send_file_response)

    doc_io = io.BytesIO(b"fake document data")

    r = ym_helper.sync_send_file(
        document=doc_io, filename="test_document.pdf", login="test_user"
    )

    assert r["ok"] is True
    assert r["message_id"] == 12347


@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
def test_sync_helper_get_updates(httpx_mock: HTTPXMock):
    """Тест получения обновлений"""

    def get_updates_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "ok": True,
                "updates": [
                    {
                        "update_id": 1,
                        "message_id": 100,
                        "timestamp": 1706620800,
                        "from": {"login": "user1"},
                        "chat": {"type": "private"},
                        "text": "Message 1",
                    },
                    {
                        "update_id": 2,
                        "message_id": 101,
                        "timestamp": 1706620801,
                        "from": {"login": "user2"},
                        "chat": {"type": "private"},
                        "text": "Message 2",
                    },
                ],
            },
        )

    httpx_mock.add_callback(get_updates_response)

    r = ym_helper.sync_get_updates(limit=100, offset=0)

    assert r["ok"] is True
    assert len(r["updates"]) == 2
    assert r["updates"][0]["text"] == "Message 1"
    assert r["updates"][1]["text"] == "Message 2"


@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
def test_sync_helper_set_webhook(httpx_mock: HTTPXMock):
    """Тест установки webhook"""

    def set_webhook_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True})

    httpx_mock.add_callback(set_webhook_response)

    r = ym_helper.sync_set_webhook(webhook_url="https://example.com/webhook")

    assert r["ok"] is True


@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
def test_sync_helper_delete_webhook(httpx_mock: HTTPXMock):
    """Тест удаления webhook"""

    def delete_webhook_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True})

    httpx_mock.add_callback(delete_webhook_response)

    r = ym_helper.sync_set_webhook(webhook_url=None)

    assert r["ok"] is True


# === ASYNC TESTS ===


@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
async def test_async_helper_send_text(httpx_mock: HTTPXMock):
    """Тест асинхронной отправки текста"""

    def send_text_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "message_id": 12345})

    httpx_mock.add_callback(send_text_response)

    r = await ym_helper.async_send_text(text="Async test message", login="test_user")

    assert r["ok"] is True
    assert r["message_id"] == 12345


@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
async def test_async_helper_send_image(httpx_mock: HTTPXMock):
    """Тест асинхронной отправки изображения"""

    def send_image_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"ok": True, "message_id": 12346})

    httpx_mock.add_callback(send_image_response)

    image_io = io.BytesIO(b"fake async image data")

    r = await ym_helper.async_send_image(image=image_io, login="test_user")

    assert r["ok"] is True
    assert r["message_id"] == 12346


@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
async def test_async_helper_get_updates(httpx_mock: HTTPXMock):
    """Тест асинхронного получения обновлений"""

    def get_updates_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "ok": True,
                "updates": [
                    {
                        "update_id": 1,
                        "message_id": 100,
                        "timestamp": 1706620800,
                        "from": {"login": "async_user"},
                        "chat": {"type": "private"},
                        "text": "Async message",
                    }
                ],
            },
        )

    httpx_mock.add_callback(get_updates_response)

    r = await ym_helper.async_get_updates()

    assert r["ok"] is True
    assert len(r["updates"]) == 1
    assert r["updates"][0]["text"] == "Async message"


def test_parse_updates():
    """Тест вспомогательного метода parse_updates"""
    response = {
        "ok": True,
        "updates": [
            {
                "update_id": 1,
                "message_id": 100,
                "timestamp": 1706620800,
                "from": {"login": "user1"},
                "chat": {"type": "private"},
                "text": "Message 1",
            },
            {
                "update_id": 2,
                "message_id": 101,
                "timestamp": 1706620801,
                "from": {"login": "user2"},
                "chat": {"type": "group", "id": "group_123"},
                "text": "Message 2",
            },
        ],
    }

    updates = ym_helper.parse_updates(response)

    assert len(updates) == 2
    assert updates[0].update_id == 1
    assert updates[0].text == "Message 1"
    assert updates[1].chat.id == "group_123"
