import pytest

from multibotkit.dispatchers.telegram import TelegramDispatcher
from multibotkit.schemas.telegram.incoming import Message, Update
from multibotkit.states.state import State


@pytest.mark.asyncio
async def test_telegram_dispatcher():

    test_results = {
        1: False,
        2: False
    }

    dp = TelegramDispatcher()

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
        state_object_func=lambda state_object: state_object.state is None
    )
    async def test_handler_1(update: Update, state_object: State):
        test_results[1] = True
        await state_object.set_state(state="state")

    @dp.handler(
        func=lambda update: update.message.text.startswith("text"),
        state_object_func=lambda state_object: state_object.state == "state",
    )
    async def test_handler_2(update: Update, state_object: State):
        test_results[2] = True

    await dp.process_event(event=update)
    await dp.process_event(event=update)

    assert test_results[1]
    assert test_results[2]
