import pytest

from multibotkit.dispatchers.fb import FacebookDispatcher
from multibotkit.schemas.fb.incoming import IncomingEvent


@pytest.mark.asyncio
async def test_fb_dispatcher():

    test_results = {1: False, 2: False}

    dp = FacebookDispatcher()

    state_data = {"state": "state"}

    event_entry_message_recipient_dict = {"id": "id"}

    event_entry_message_sender_dict = {"id": "id"}

    message_attachment_payload_dict = {"url": "url"}

    message_attachment_dict = {
        "type": "type",
        "payload": message_attachment_payload_dict,
    }

    event_entry_message_data_dict = {
        "mid": "mid",
        "text": "text",
        "attachments": [message_attachment_dict],
    }

    referral_data_dict = {"ref": "ref", "source": "source", "type": "type"}

    message_postback_dict = {
        "title": "title",
        "payload": "payload",
        "referral": referral_data_dict,
    }

    event_entry_message_dict = {
        "sender": event_entry_message_sender_dict,
        "recipient": event_entry_message_recipient_dict,
        "timestamp": 60000,
        "message": event_entry_message_data_dict,
        "postback": message_postback_dict,
        "referral": referral_data_dict,
    }

    event_entry_message_dict = {
        "sender": event_entry_message_sender_dict,
        "recipient": event_entry_message_recipient_dict,
        "timestamp": 60000,
        "message": event_entry_message_data_dict,
        "postback": message_postback_dict,
        "referral": referral_data_dict,
    }

    event_entry_dict = {
        "id": "id",
        "time": 60000,
        "messaging": [event_entry_message_dict],
    }

    incoming_event_dict = {"object": "object", "entry": [event_entry_dict]}

    update = IncomingEvent.parse_obj(incoming_event_dict)

    @dp.handler(
        func=lambda update: update.entry[0]
        .messaging[0]
        .message.text.startswith("text"),
        state_object_func=lambda state_object: state_object.state is None,
    )
    async def test_handler_1(update: IncomingEvent, state_object: dict):
        test_results[1] = True
        await state_object.set_state(state="state")

    @dp.handler(
        func=lambda update: update.entry[0]
        .messaging[0]
        .message.text.startswith("text"),
        state_object_func=lambda state_object: state_object.state == "state",
    )
    async def test_handler_2(update: IncomingEvent, state_object: dict):
        test_results[2] = True

    await dp.process_event(update, state_data)
    await dp.process_event(update, state_data)

    assert test_results[1]
    assert test_results[2]
