import pytest

from multibotkit.dispatchers.vk import VkontakteDispatcher
from multibotkit.schemas.vk.incoming import IncomingEvent


@pytest.mark.asyncio
async def test_dispatcher():
    dp = VkontakteDispatcher()

    client_info_dict = {
        "button_actions": [],
        "carousel": False,
        "inline_keyboard": False,
        "keyboard": False,
        "lang_id": 1234,
    }

    coordinates_object_dict = {"longitude": 59.769595, "latitude": 30.796399}

    geo_object_dict = {
        "type": "geo object type",
        "coordinates": coordinates_object_dict,
    }

    message_object_dict = {
        "attachments": [],
        "conversation_message_id": 1234,
        "date": 1656425873,
        "from_id": "from id",
        "peer_id": "peer id",
        "random_id": 1111,
        "fwd_messages": [],
        "ref": "ref",
        "id": 2222,
        "out": 3333,
        "important": False,
        "is_hidden": False,
        "text": "text",
        "payload": "payload",
        "geo": geo_object_dict,
    }

    event_object_dict = {
        "client_info": client_info_dict,
        "message": message_object_dict,
    }

    incoming_event_dict = {
        "type": "event type",
        "group_id": 1234,
        "object": event_object_dict,
    }

    incoming_event = IncomingEvent.parse_obj(incoming_event_dict)

    state_data = {"state": "state"}

    @dp.register_handler(
        func=lambda event: event.object.message.text.startswith("text"),
        state_data_func=lambda state_data: state_data["state"] == "state",
    )
    async def test_handler(event: IncomingEvent, state_data: dict):
        assert True

    await dp.process_event(incoming_event, state_data)
