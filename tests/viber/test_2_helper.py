import httpx
import pytest
from pytest_httpx import HTTPXMock

from multibotkit.helpers.viber import ViberHelper
from multibotkit.schemas.viber.outgoing import (
    Button,
    Contact,
    Keyboard,
    Location,
    Sender,
    SetWebhook,
)
from tests.config import settings


viber_helper = ViberHelper(token=settings.VIBER_TOKEN)


def test_sync_set_webhook(httpx_mock: HTTPXMock):
    def set_webhook_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "status": 0,
                "status_message": "ok",
                "event_types": [
                    "delivered",
                    "seen",
                    "failed",
                    "subscribed",
                    "unsubscribed",
                    "conversation_started",
                ],
            },
        )

    httpx_mock.add_callback(set_webhook_response)

    set_webhook_data = SetWebhook(
        url="url", event_types=["event_type"], send_name=True, send_photo=False
    )

    r = viber_helper.sync_set_webhook(webhook_data=set_webhook_data)

    assert r == {
        "status": 0,
        "status_message": "ok",
        "event_types": [
            "delivered",
            "seen",
            "failed",
            "subscribed",
            "unsubscribed",
            "conversation_started",
        ],
    }


def test_sync_get_account_info(httpx_mock: HTTPXMock):
    def get_account_info_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "status": 0,
                "status_message": "ok",
                "id": "pa:75346594275468546724",
                "name": "account name",
                "uri": "accountUri",
                "icon": "http://example.com",
                "background": "http://example.com",
                "category": "category",
                "subcategory": "sub category",
                "location": {"lon": 0.1, "lat": 0.2},
                "country": "UK",
                "webhook": "https://my.site.com",
                "event_types": ["delivered", "seen"],
                "subscribers_count": 35,
                "members": [
                    {
                        "id": "01234567890A=",
                        "name": "my name",
                        "avatar": "http://example.com",
                        "role": "admin",
                    }
                ],
            },
        )

    httpx_mock.add_callback(get_account_info_response)

    r = viber_helper.sync_get_account_info()

    assert r == {
        "status": 0,
        "status_message": "ok",
        "id": "pa:75346594275468546724",
        "name": "account name",
        "uri": "accountUri",
        "icon": "http://example.com",
        "background": "http://example.com",
        "category": "category",
        "subcategory": "sub category",
        "location": {"lon": 0.1, "lat": 0.2},
        "country": "UK",
        "webhook": "https://my.site.com",
        "event_types": ["delivered", "seen"],
        "subscribers_count": 35,
        "members": [
            {
                "id": "01234567890A=",
                "name": "my name",
                "avatar": "http://example.com",
                "role": "admin",
            }
        ],
    }


def test_sync_send_message(httpx_mock: HTTPXMock):
    def send_message_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={})

    httpx_mock.add_callback(send_message_response)
    httpx_mock.add_callback(send_message_response)
    httpx_mock.add_callback(send_message_response)
    httpx_mock.add_callback(send_message_response)
    httpx_mock.add_callback(send_message_response)
    httpx_mock.add_callback(send_message_response)
    httpx_mock.add_callback(send_message_response)
    httpx_mock.add_callback(send_message_response)

    button = Button(
        Columns=1,
        Rows=1,
        Text="text",
        TextSize="10",
        TextHAlign="text H align",
        TextVAlign="text V align",
        ActionType="action type",
        ActionBody="action body",
        BgColor="bg color",
        Image="image",
    )

    keyboard = Keyboard(
        Type="type", DefaultHeight=True, BgColor="bg color", Buttons=[button]
    )

    sender = Sender(name="name", avatar="avatar")

    contact = Contact(
        name="name",
        phone_number="89999999999"
    )

    location = Location(
        lat=0,
        lon=0
    )

    r = viber_helper.sync_send_message(
        type="text",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        text="text"
    )
    
    assert r == {}
    
    r = viber_helper.sync_send_message(
        type="picture",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        text="text",
        media="media"
    )
    
    assert r == {}
    
    r = viber_helper.sync_send_message(
        type="video",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        media="media",
        size=512
    )
    
    assert r == {}
    
    r = viber_helper.sync_send_message(
        type="file",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        media="media",
        size=512,
        file_name="file name"
    )
    
    assert r == {}
    
    r = viber_helper.sync_send_message(
        type="contact",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        contact=contact
    )
    
    assert r == {}
    
    r = viber_helper.sync_send_message(
        type="location",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        location=location
    )
    
    assert r == {}
    
    r = viber_helper.sync_send_message(
        type="url",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        media="media"
    )
    
    assert r == {}
    
    r = viber_helper.sync_send_message(
        type="sticker",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        sticker_id=1234
    )

    assert r == {}


def test_sync_send_message_arguments_errors():

    button = Button(
        Columns=1,
        Rows=1,
        Text="text",
        TextSize="10",
        TextHAlign="text H align",
        TextVAlign="text V align",
        ActionType="action type",
        ActionBody="action body",
        BgColor="bg color",
        Image="image",
    )

    keyboard = Keyboard(
        Type="type", DefaultHeight=True, BgColor="bg color", Buttons=[button]
    )

    sender = Sender(name="name", avatar="avatar")

    try:
        _ = viber_helper.sync_send_message(
            type="text",
            receiver="receiver",
            sender=sender,
            tracking_data="tracking data",
            keyboard=keyboard
        )
        
        assert False

    except viber_helper._SendMessageArgumentsError:
        assert True

    try:
        _ = viber_helper.sync_send_message(
            type="picture",
            receiver="receiver",
            sender=sender,
            tracking_data="tracking data",
            keyboard=keyboard
        )

        assert False

    except viber_helper._SendMessageArgumentsError:
        assert True
    
    try:
        _ = viber_helper.sync_send_message(
            type="video",
            receiver="receiver",
            sender=sender,
            tracking_data="tracking data",
            keyboard=keyboard
        )

        assert False

    except viber_helper._SendMessageArgumentsError:
        assert True
    
    try:
        _ = viber_helper.sync_send_message(
            type="file",
            receiver="receiver",
            sender=sender,
            tracking_data="tracking data",
            keyboard=keyboard
        )

        assert False

    except viber_helper._SendMessageArgumentsError:
        assert True
    
    try:
        _ = viber_helper.sync_send_message(
            type="contact",
            receiver="receiver",
            sender=sender,
            tracking_data="tracking data",
            keyboard=keyboard
        )

        assert False

    except viber_helper._SendMessageArgumentsError:
        assert True
    
    try:
        _ = viber_helper.sync_send_message(
            type="location",
            receiver="receiver",
            sender=sender,
            tracking_data="tracking data",
            keyboard=keyboard
        )

        assert False

    except viber_helper._SendMessageArgumentsError:
        assert True
    
    try:
        _ = viber_helper.sync_send_message(
            type="url",
            receiver="receiver",
            sender=sender,
            tracking_data="tracking data",
            keyboard=keyboard
        )

        assert False

    except viber_helper._SendMessageArgumentsError:
        assert True
    
    try:
        _ = viber_helper.sync_send_message(
            type="sticker",
            receiver="receiver",
            sender=sender,
            tracking_data="tracking data",
            keyboard=keyboard
        )

        assert False

    except viber_helper._SendMessageArgumentsError:
        assert True


@pytest.mark.asyncio
async def test_async_set_webhook(httpx_mock: HTTPXMock):
    def set_webhook_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "status": 0,
                "status_message": "ok",
                "event_types": [
                    "delivered",
                    "seen",
                    "failed",
                    "subscribed",
                    "unsubscribed",
                    "conversation_started",
                ],
            },
        )

    httpx_mock.add_callback(set_webhook_response)

    set_webhook_data = SetWebhook(
        url="url", event_types=["event_type"], send_name=True, send_photo=False
    )

    r = await viber_helper.async_set_webhook(webhook_data=set_webhook_data)

    assert r == {
        "status": 0,
        "status_message": "ok",
        "event_types": [
            "delivered",
            "seen",
            "failed",
            "subscribed",
            "unsubscribed",
            "conversation_started",
        ],
    }


@pytest.mark.asyncio
async def test_async_get_account_info(httpx_mock: HTTPXMock):
    def get_account_info_response(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={
                "status": 0,
                "status_message": "ok",
                "id": "pa:75346594275468546724",
                "name": "account name",
                "uri": "accountUri",
                "icon": "http://example.com",
                "background": "http://example.com",
                "category": "category",
                "subcategory": "sub category",
                "location": {"lon": 0.1, "lat": 0.2},
                "country": "UK",
                "webhook": "https://my.site.com",
                "event_types": ["delivered", "seen"],
                "subscribers_count": 35,
                "members": [
                    {
                        "id": "01234567890A=",
                        "name": "my name",
                        "avatar": "http://example.com",
                        "role": "admin",
                    }
                ],
            },
        )

    httpx_mock.add_callback(get_account_info_response)

    r = await viber_helper.async_get_account_info()

    assert r == {
        "status": 0,
        "status_message": "ok",
        "id": "pa:75346594275468546724",
        "name": "account name",
        "uri": "accountUri",
        "icon": "http://example.com",
        "background": "http://example.com",
        "category": "category",
        "subcategory": "sub category",
        "location": {"lon": 0.1, "lat": 0.2},
        "country": "UK",
        "webhook": "https://my.site.com",
        "event_types": ["delivered", "seen"],
        "subscribers_count": 35,
        "members": [
            {
                "id": "01234567890A=",
                "name": "my name",
                "avatar": "http://example.com",
                "role": "admin",
            }
        ],
    }


@pytest.mark.asyncio
async def test_async_send_message(httpx_mock: HTTPXMock):
    def send_message_response(request: httpx.Request):
        return httpx.Response(status_code=200, json={})

    httpx_mock.add_callback(send_message_response)

    button = Button(
        Columns=1,
        Rows=1,
        Text="text",
        TextSize="10",
        TextHAlign="text H align",
        TextVAlign="text V align",
        ActionType="action type",
        ActionBody="action body",
        BgColor="bg color",
        Image="image",
    )

    keyboard = Keyboard(
        Type="type", DefaultHeight=True, BgColor="bg color", Buttons=[button]
    )

    sender = Sender(name="name", avatar="avatar")

    r = await viber_helper.async_send_message(
        type="text",
        receiver="receiver",
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        text="text"
    )

    assert r == {}
