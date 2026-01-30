import pytest

from multibotkit.dispatchers.yandexmessenger import YandexMessengerDispatcher
from multibotkit.schemas.yandexmessenger.incoming import (
    Chat,
    ChatType,
    Image,
    Sender,
    Update,
)
from multibotkit.states.state import State


@pytest.mark.asyncio
async def test_yandexmessenger_dispatcher_text_message():
    """Тест обработки текстового сообщения с state machine"""
    test_results = {1: False, 2: False}

    dp = YandexMessengerDispatcher()

    update = Update(
        update_id=1,
        message_id=100,
        timestamp=1706620800,
        from_=Sender(login="test_user", display_name="Test User", robot=False),
        chat=Chat(type=ChatType.private),
        text="Hello",
    )

    @dp.handler(
        func=lambda update: update.text.startswith("Hello"),
        state_object_func=lambda state: state.state is None,
    )
    async def handler_1(update: Update, state: State):
        test_results[1] = True
        await state.set_state(state="waiting")

    @dp.handler(
        func=lambda update: update.text.startswith("Hello"),
        state_object_func=lambda state: state.state == "waiting",
    )
    async def handler_2(update: Update, state: State):
        test_results[2] = True

    await dp.process_event(event=update)
    await dp.process_event(event=update)

    assert test_results[1]
    assert test_results[2]


@pytest.mark.asyncio
async def test_yandexmessenger_dispatcher_with_images():
    """Тест обработки сообщения с изображениями"""
    test_results = {"handler_called": False, "images_count": 0}

    dp = YandexMessengerDispatcher()

    image1 = Image(file_id="img_123", width=800, height=600, size=102400, name="photo.jpg")
    image2 = Image(file_id="img_456", width=1920, height=1080, size=524288, name="big_photo.jpg")

    update = Update(
        update_id=2,
        message_id=101,
        timestamp=1706620801,
        from_=Sender(login="photo_user", display_name="Photo User", robot=False),
        chat=Chat(type=ChatType.private),
        text="Check these photos",
        images=[image1, image2],
    )

    @dp.handler(
        func=lambda update: update.images is not None and len(update.images) > 0,
    )
    async def image_handler(update: Update, state: State):
        test_results["handler_called"] = True
        test_results["images_count"] = len(update.images)

    await dp.process_event(event=update)

    assert test_results["handler_called"]
    assert test_results["images_count"] == 2


@pytest.mark.asyncio
async def test_yandexmessenger_dispatcher_group_chat():
    """Тест обработки сообщения из группового чата"""
    test_results = {"chat_type": None, "chat_id": None}

    dp = YandexMessengerDispatcher()

    update = Update(
        update_id=3,
        message_id=102,
        timestamp=1706620802,
        from_=Sender(login="group_user", display_name="Group User", robot=False),
        chat=Chat(type=ChatType.group, id="group_12345"),
        text="Group message",
    )

    @dp.handler(
        func=lambda update: update.chat.type == ChatType.group,
    )
    async def group_handler(update: Update, state: State):
        test_results["chat_type"] = update.chat.type
        test_results["chat_id"] = update.chat.id

    await dp.process_event(event=update)

    assert test_results["chat_type"] == ChatType.group
    assert test_results["chat_id"] == "group_12345"


@pytest.mark.asyncio
async def test_yandexmessenger_dispatcher_state_machine():
    """Тест полного сценария state machine: start → name → age"""
    test_results = {
        "start_called": False,
        "name_called": False,
        "age_called": False,
        "final_name": None,
        "final_age": None,
    }

    dp = YandexMessengerDispatcher()

    # Сообщение 1: /start
    update_start = Update(
        update_id=4,
        message_id=103,
        timestamp=1706620803,
        from_=Sender(login="flow_user", display_name="Flow User", robot=False),
        chat=Chat(type=ChatType.private),
        text="/start",
    )

    # Сообщение 2: имя пользователя
    update_name = Update(
        update_id=5,
        message_id=104,
        timestamp=1706620804,
        from_=Sender(login="flow_user", display_name="Flow User", robot=False),
        chat=Chat(type=ChatType.private),
        text="John",
    )

    # Сообщение 3: возраст
    update_age = Update(
        update_id=6,
        message_id=105,
        timestamp=1706620805,
        from_=Sender(login="flow_user", display_name="Flow User", robot=False),
        chat=Chat(type=ChatType.private),
        text="25",
    )

    @dp.handler(
        func=lambda update: update.text == "/start",
        state_object_func=lambda state: state.state is None,
    )
    async def start_handler(update: Update, state: State):
        test_results["start_called"] = True
        await state.set_state(state="waiting_name")

    @dp.handler(
        func=lambda update: update.text is not None,
        state_object_func=lambda state: state.state == "waiting_name",
    )
    async def name_handler(update: Update, state: State):
        test_results["name_called"] = True
        await state.set_state(state="waiting_age", state_data={"name": update.text})

    @dp.handler(
        func=lambda update: update.text is not None and update.text.isdigit(),
        state_object_func=lambda state: state.state == "waiting_age",
    )
    async def age_handler(update: Update, state: State):
        test_results["age_called"] = True
        test_results["final_name"] = state.data.get("name")
        test_results["final_age"] = int(update.text)
        await state.set_state(state="completed", state_data={**state.data, "age": int(update.text)})

    # Выполнение сценария
    await dp.process_event(event=update_start)
    await dp.process_event(event=update_name)
    await dp.process_event(event=update_age)

    assert test_results["start_called"]
    assert test_results["name_called"]
    assert test_results["age_called"]
    assert test_results["final_name"] == "John"
    assert test_results["final_age"] == 25


@pytest.mark.asyncio
async def test_yandexmessenger_dispatcher_sender_with_id():
    """Тест обработки сообщений от ботов/каналов (с id вместо login)"""
    test_results = {"sender_id": None, "is_robot": None}

    dp = YandexMessengerDispatcher()

    update = Update(
        update_id=7,
        message_id=106,
        timestamp=1706620806,
        from_=Sender(id="bot_12345", display_name="Test Bot", robot=True),
        chat=Chat(type=ChatType.private),
        text="Bot message",
    )

    @dp.handler(
        func=lambda update: update.from_.robot is True,
    )
    async def bot_handler(update: Update, state: State):
        test_results["sender_id"] = update.from_.id
        test_results["is_robot"] = update.from_.robot

    await dp.process_event(event=update)

    assert test_results["sender_id"] == "bot_12345"
    assert test_results["is_robot"] is True


@pytest.mark.asyncio
async def test_yandexmessenger_dispatcher_multiple_handlers():
    """Тест что выполняется только первый подходящий handler"""
    execution_order = []

    dp = YandexMessengerDispatcher()

    update = Update(
        update_id=8,
        message_id=107,
        timestamp=1706620807,
        from_=Sender(login="multi_user", display_name="Multi User", robot=False),
        chat=Chat(type=ChatType.private),
        text="test",
    )

    @dp.handler(func=lambda update: True)
    async def handler_1(update: Update, state: State):
        execution_order.append(1)

    @dp.handler(func=lambda update: True)
    async def handler_2(update: Update, state: State):
        execution_order.append(2)

    @dp.handler(func=lambda update: True)
    async def handler_3(update: Update, state: State):
        execution_order.append(3)

    await dp.process_event(event=update)

    # Должен выполниться только первый handler
    assert len(execution_order) == 1
    assert execution_order[0] == 1
