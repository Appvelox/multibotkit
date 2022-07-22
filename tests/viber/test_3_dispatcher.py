import pytest

from multibotkit.dispatchers.viber import ViberDispatcher
from multibotkit.schemas.viber.incoming import Callback


@pytest.mark.asyncio
async def test_telegram_dispatcher():

    dp = ViberDispatcher()

    state_data = {"state": "state"}

    contact_dict = {"name": "Name", "phone_number": "89999999999", "avatar": "avatar"}

    location_dict = {"lat": "+90°", "lon": "-180°"}

    message_dict = {
        "type": "text",
        "text": "text",
        "media": "media",
        "location": location_dict,
        "contact": contact_dict,
        "tracking_data": "tracking data",
        "file_name": "file name",
        "file_size": 512,
        "duration": 60,
        "sticker_id": 1234,
    }

    user_dict = {
        "id": "user id",
        "name": "Name",
        "avatar": "avatar",
        "country": "RU",
        "language": "ru",
        "api_version": 1111,
    }

    callback_dict = {
        "user_id": "user id",
        "desc": "desc",
        "type": "type",
        "context": "context",
        "user": user_dict,
        "subscribed": False,
        "sender": user_dict,
        "message": message_dict,
        "event": "event",
        "timestamp": 6000000,
        "message_token": 1234,
    }

    event = Callback.parse_obj(callback_dict)

    @dp.handler(
        func=lambda update: update.message.text.startswith("text"),
        state_data_func=lambda state_data: state_data["state"] == "state",
    )
    async def test_handler(event: Callback, state_data: dict):
        assert True

    await dp.process_event(event, state_data)
