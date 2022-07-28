from io import BytesIO
import httpx
import pytest
from pytest_httpx import HTTPXMock

from multibotkit.helpers.vk import VKHelper
from multibotkit.schemas.vk.outgoing import (
    Keyboard,
    KeyboardAction,
    KeyboardButton,
)
from tests.config import settings


vk_helper = VKHelper(
    access_token=settings.VK_TOKEN, api_version=settings.VK_API_VERSION
)


def test_button_code_and_command():
    json_payload = '{"button":"button code", "command":"command"}'

    button_code = vk_helper.button_code(json_payload)
    assert button_code == "button code"

    command = vk_helper.command(json_payload)
    assert command == "command"

    json_payload = None

    button_code = vk_helper.button_code(json_payload)
    assert button_code == ""

    command = vk_helper.command(json_payload)
    assert command == ""


def test_syncSendMessage(httpx_mock: HTTPXMock):
    def send_message_response(request: httpx.Request):
        return httpx.Response(
            status_code=200, json={"peer_id": 1234, "message_id": 4321}
        )

    httpx_mock.add_callback(send_message_response)

    keyboard_action = KeyboardAction(type="type", label="label", payload="payload")

    keyboard_button = KeyboardButton(action=keyboard_action, color="color")

    keyboard = Keyboard(one_time=False, inline=True, buttons=[[keyboard_button]])

    r = vk_helper.syncSendMessage(
        user_id=1234,
        text="message",
        keyboard=keyboard,
        lat=0,
        long=0,
        attachment="attachment",
        template={}
    )

    assert r == {"peer_id": 1234, "message_id": 4321}


def test_syncSendMessageArgumentsError():
    try:
        _ = vk_helper.syncSendMessage(
            user_id=1234
        )
        assert False
    except vk_helper._SendMessageArgumentsError:
        assert True


def test_syncUploadPhoto(httpx_mock: HTTPXMock):
    def upload_photo_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "upload_url": "upload_url",
                "album_id": "album_id",
                "group_id": "group_id",
            },
        )

    httpx_mock.add_callback(upload_photo_response)

    image = BytesIO()

    r = vk_helper.syncUploadPhoto(
        photo=image, file_name="photo.img", server_url="https://server_url"
    )

    assert r == {
        "upload_url": "upload_url",
        "album_id": "album_id",
        "group_id": "group_id",
    }


def test_syncSavePhoto(httpx_mock: HTTPXMock):
    def save_photo_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "response": [
                    {
                        "id": "id",
                        "pid": "pid",
                        "aid": "aid",
                        "owner_id": "owner_id",
                        "src": "src",
                        "src_big": "src_big",
                        "src_small": "src_small",
                        "created": "created",
                    }
                ]
            },
        )

    httpx_mock.add_callback(save_photo_response)

    r = vk_helper.syncSavePhoto(uploaded_photo={})

    assert r == {
        "id": "id",
        "pid": "pid",
        "aid": "aid",
        "owner_id": "owner_id",
        "src": "src",
        "src_big": "src_big",
        "src_small": "src_small",
        "created": "created",
    }


def test_syncGetPhotoAttachment(httpx_mock: HTTPXMock):
    def get_url_response(request: httpx.Request):
        return httpx.Response(
            status_code=200, json={"response": {"upload_url": "https://upload_url"}}
        )

    def upload_photo_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "upload_url": "upload_url",
                "album_id": "album_id",
                "group_id": "group_id",
            },
        )

    def save_photo_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "response": [
                    {
                        "id": "id",
                        "pid": "pid",
                        "aid": "aid",
                        "owner_id": "owner_id",
                        "src": "src",
                        "src_big": "src_big",
                        "src_small": "src_small",
                        "created": "created",
                        "access_key": "access_key",
                    }
                ]
            },
        )

    httpx_mock.add_callback(get_url_response)
    httpx_mock.add_callback(upload_photo_response)
    httpx_mock.add_callback(save_photo_response)

    image = BytesIO()

    r = vk_helper.syncGetPhotoAttachment(photo=image, file_name="photo.img")

    assert r == "photoowner_id_id_access_key"


@pytest.mark.asyncio
async def test_asyncSendMessage(httpx_mock: HTTPXMock):
    def send_message_response(request: httpx.Request):
        return httpx.Response(
            status_code=200, json={"peer_id": 1234, "message_id": 4321}
        )

    httpx_mock.add_callback(send_message_response)

    keyboard_action = KeyboardAction(type="type", label="label", payload="payload")

    keyboard_button = KeyboardButton(action=keyboard_action, color="color")

    keyboard = Keyboard(one_time=False, inline=True, buttons=[[keyboard_button]])

    r = vk_helper.syncSendMessage(
        user_id=1234,
        text="message",
        keyboard=keyboard,
        lat=0,
        long=0,
        attachment="attachment",
        template={}
    )

    assert r == {"peer_id": 1234, "message_id": 4321}


@pytest.mark.asyncio
async def test_asyncUploadPhoto(httpx_mock: HTTPXMock):
    def upload_photo_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "upload_url": "upload_url",
                "album_id": "album_id",
                "group_id": "group_id",
            },
        )

    httpx_mock.add_callback(upload_photo_response)

    image = BytesIO()

    r = await vk_helper.asyncUploadPhoto(
        photo=image, file_name="photo.img", server_url="https://server_url"
    )

    assert r == {
        "upload_url": "upload_url",
        "album_id": "album_id",
        "group_id": "group_id",
    }


@pytest.mark.asyncio
async def test_asyncSavePhoto(httpx_mock: HTTPXMock):
    def save_photo_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "response": [
                    {
                        "id": "id",
                        "pid": "pid",
                        "aid": "aid",
                        "owner_id": "owner_id",
                        "src": "src",
                        "src_big": "src_big",
                        "src_small": "src_small",
                        "created": "created",
                    }
                ]
            },
        )

    httpx_mock.add_callback(save_photo_response)

    r = await vk_helper.asyncSavePhoto(uploaded_photo={})

    assert r == {
        "id": "id",
        "pid": "pid",
        "aid": "aid",
        "owner_id": "owner_id",
        "src": "src",
        "src_big": "src_big",
        "src_small": "src_small",
        "created": "created",
    }


@pytest.mark.asyncio
async def test_asyncGetPhotoAttachment(httpx_mock: HTTPXMock):
    def get_url_response(request: httpx.Request):
        return httpx.Response(
            status_code=200, json={"response": {"upload_url": "https://upload_url"}}
        )

    def upload_photo_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "upload_url": "upload_url",
                "album_id": "album_id",
                "group_id": "group_id",
            },
        )

    def save_photo_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "response": [
                    {
                        "id": "id",
                        "pid": "pid",
                        "aid": "aid",
                        "owner_id": "owner_id",
                        "src": "src",
                        "src_big": "src_big",
                        "src_small": "src_small",
                        "created": "created",
                        "access_key": "access_key",
                    }
                ]
            },
        )

    httpx_mock.add_callback(get_url_response)
    httpx_mock.add_callback(upload_photo_response)
    httpx_mock.add_callback(save_photo_response)

    image = BytesIO()

    r = await vk_helper.asyncGetPhotoAttachment(photo=image, file_name="photo.img")

    assert r == "photoowner_id_id_access_key"
