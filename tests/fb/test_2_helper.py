import json

import httpx
import pytest
from pytest_httpx import HTTPXMock

from multibotkit.helpers.fb import FBHelper
from multibotkit.schemas.fb.outgoing import Message, PersistentMenu
from tests.config import settings


fb_helper = FBHelper(
    messages_endpoint=settings.FB_MESSAGES_ENDPOINT,
    profile_endpoint=settings.FB_PROFILE_ENDPOINT,
    token=settings.FB_PAGE_TOKEN,
)


def test_sync_send_message(httpx_mock: HTTPXMock):
    def send_message_response(request: httpx.Request):
        content = json.loads(json.loads(request.content.decode()))
        return httpx.Response(
            status_code=200,
            json={
                "recipient_id": content["recipient"]["id"],
                "message_id": "AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P",
            },
        )

    httpx_mock.add_callback(send_message_response)

    generic_template_button_dict = {
        "type": "type",
        "title": "title",
        "payload": "payload",
        "url": "url",
    }

    generic_template_element_dict = {
        "title": "title",
        "image_url": "image url",
        "subtitle": "subtitle",
        "buttons": [generic_template_button_dict],
    }

    quick_reply_dict = {
        "content_type": "content type",
        "title": "title",
        "payload": "payload",
        "image_url": "image url",
    }

    message_data_attachment_payload_dict = {
        "template_type": "template type",
        "text": "text",
        "buttons": [generic_template_button_dict],
        "elements": [generic_template_element_dict],
    }

    message_data_attachment_dict = {
        "type": "type",
        "payload": message_data_attachment_payload_dict,
    }

    message_data_dict = {
        "text": "text",
        "attachment": message_data_attachment_dict,
        "quick_replies": [quick_reply_dict],
    }

    message_recipient_dict = {"id": "id", "email": "e-mail"}

    message_dict = {
        "recipient": message_recipient_dict,
        "messaging_type": "messaging type",
        "message": message_data_dict,
    }

    message = Message.parse_obj(message_dict)

    r = fb_helper.sync_send_message(message=message)

    assert r == {
        "recipient_id": "id",
        "message_id": "AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P",
    }


def test_sync_send_get_started(httpx_mock: HTTPXMock):
    def send_get_started_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"result": "success"})

    httpx_mock.add_callback(send_get_started_response)

    r = fb_helper.sync_send_get_started()

    assert r == {"result": "success"}


def test_sync_send_greeting(httpx_mock: HTTPXMock):
    def send_greeting_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"result": "success"})

    httpx_mock.add_callback(send_greeting_response)

    r = fb_helper.sync_send_greeting(text="text")

    assert r == {"result": "success"}


def test_sync_send_persistent_menu(httpx_mock: HTTPXMock):
    def send_persistent_menu_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"result": "success"})

    httpx_mock.add_callback(send_persistent_menu_response)

    menu_item_dict = {
        "type": "type",
        "title": "title",
        "url": "url",
        "payload": "payload",
        "webview_height_ratio": "webview height ratio",
        "messenger_extensions": False,
        "fallback_url": "fallback url",
        "webview_share_button": "webview share button"
    }

    persistent_menu_element_dict = {
        "locale": "locale",
        "composer_input_disabled": False,
        "disabled_surfaces": ["disabled surface"],
        "call_to_actions": [menu_item_dict]
    }

    persistent_menu_dict = {
        "persistent_menu": [persistent_menu_element_dict]
    }

    persistent_menu = PersistentMenu.parse_obj(persistent_menu_dict)

    r = fb_helper.sync_send_persistent_menu(persistent_menu)

    assert r == {"result": "success"}


@pytest.mark.asyncio
async def test_async_send_message(httpx_mock: HTTPXMock):
    def send_message_response(request: httpx.Request):
        content = json.loads(json.loads(request.content.decode()))
        return httpx.Response(
            status_code=200,
            json={
                "recipient_id": content["recipient"]["id"],
                "message_id": "AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P",
            },
        )

    httpx_mock.add_callback(send_message_response)

    generic_template_button_dict = {
        "type": "type",
        "title": "title",
        "payload": "payload",
        "url": "url",
    }

    generic_template_element_dict = {
        "title": "title",
        "image_url": "image url",
        "subtitle": "subtitle",
        "buttons": [generic_template_button_dict],
    }

    quick_reply_dict = {
        "content_type": "content type",
        "title": "title",
        "payload": "payload",
        "image_url": "image url",
    }

    message_data_attachment_payload_dict = {
        "template_type": "template type",
        "text": "text",
        "buttons": [generic_template_button_dict],
        "elements": [generic_template_element_dict],
    }

    message_data_attachment_dict = {
        "type": "type",
        "payload": message_data_attachment_payload_dict,
    }

    message_data_dict = {
        "text": "text",
        "attachment": message_data_attachment_dict,
        "quick_replies": [quick_reply_dict],
    }

    message_recipient_dict = {"id": "id", "email": "e-mail"}

    message_dict = {
        "recipient": message_recipient_dict,
        "messaging_type": "messaging type",
        "message": message_data_dict,
    }

    message = Message.parse_obj(message_dict)

    r = await fb_helper.async_send_message(message=message)

    assert r == {
        "recipient_id": "id",
        "message_id": "AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P",
    }


@pytest.mark.asyncio
async def test_async_send_get_started(httpx_mock: HTTPXMock):
    def send_get_started_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"result": "success"})

    httpx_mock.add_callback(send_get_started_response)

    r = await fb_helper.async_send_get_started()

    assert r == {"result": "success"}


@pytest.mark.asyncio
async def test_async_send_greeting(httpx_mock: HTTPXMock):
    def send_greeting_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"result": "success"})

    httpx_mock.add_callback(send_greeting_response)

    r = await fb_helper.async_send_greeting(text="text")

    assert r == {"result": "success"}


@pytest.mark.asyncio
async def test_async_send_persistent_menu(httpx_mock: HTTPXMock):
    def send_persistent_menu_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={"result": "success"})

    httpx_mock.add_callback(send_persistent_menu_response)

    menu_item_dict = {
        "type": "type",
        "title": "title",
        "url": "url",
        "payload": "payload",
        "webview_height_ratio": "webview height ratio",
        "messenger_extensions": False,
        "fallback_url": "fallback url",
        "webview_share_button": "webview share button"
    }

    persistent_menu_element_dict = {
        "locale": "locale",
        "composer_input_disabled": False,
        "disabled_surfaces": ["disabled surface"],
        "call_to_actions": [menu_item_dict]
    }

    persistent_menu_dict = {
        "persistent_menu": [persistent_menu_element_dict]
    }

    persistent_menu = PersistentMenu.parse_obj(persistent_menu_dict)

    r = await fb_helper.async_send_persistent_menu(persistent_menu)

    assert r == {"result": "success"}
