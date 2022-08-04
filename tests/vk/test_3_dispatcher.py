import pytest

from multibotkit.dispatchers.vk import VkontakteDispatcher
from multibotkit.schemas.vk.incoming import IncomingEvent


@pytest.mark.asyncio
async def test_vk_dispatcher():

    test_results = {1: False, 2: False}

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

    @dp.handler(
        func=lambda event: event.object.message.text.startswith("text"),
        state_object_func=lambda state_object: state_object.state is None,
    )
    async def test_handler_1(event: IncomingEvent, state_object: dict):
        test_results[1] = True
        await state_object.set_state(state="state")

    @dp.handler(
        func=lambda event: event.object.message.text.startswith("text"),
        state_object_func=lambda state_object: state_object.state == "state",
    )
    async def test_handler_2(event: IncomingEvent, state_object: dict):
        test_results[2] = True

    await dp.process_event(incoming_event)
    await dp.process_event(incoming_event)

    assert test_results[1]
    assert test_results[2]
