import pytest

from multibotkit.dispatchers.fb import FacebookDispatcher
from multibotkit.schemas.fb.incoming import IncomingEvent


@pytest.mark.asyncio
async def test_telegram_dispatcher():

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
        func=lambda update: update.entry.messaging.message.text.startswith("text"),
        state_data_func=lambda state_data: state_data["state"] == "state",
    )
    async def test_handler(update: IncomingEvent, state_data: dict):
        assert True

    await dp.process_event(update, state_data)
