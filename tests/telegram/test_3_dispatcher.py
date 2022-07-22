import pytest

from multibotkit.dispatchers.telegram import TelegramDispatcher
from multibotkit.schemas.telegram.incoming import Message, Update


@pytest.mark.asyncio
async def test_telegram_dispatcher():

    dp = TelegramDispatcher()

    state_data = {"state": "state"}

    user_dict = {
        "id": 1234,
        "is_bot": False,
        "first_name": "Name",
        "last_name": "Surname",
        "username": "username",
        "language_code": "ru",
        "can_join_groups": True,
        "can_read_all_group_messages": True,
        "supports_inline_queries": True,
    }

    chat_dict = {
        "id": 1234,
        "type": "group",
        "title": "title",
        "first_name": "Name",
        "last_name": "Surname",
        "username": "username",
    }

    message_dict = {
        "message_id": 1234,
        "date": 1656425873,
        "from": user_dict,
        "chat": chat_dict,
        "text": "text",
        "caption": "Caption",
    }

    update = Update(update_id=1234, message=Message.parse_obj(message_dict))

    @dp.handler(
        func=lambda update: update.message.text.startswith("text"),
        state_data_func=lambda state_data: state_data["state"] == "state",
    )
    async def test_handler(update: Update, state_data: dict):
        assert True

    await dp.process_event(update, state_data)
