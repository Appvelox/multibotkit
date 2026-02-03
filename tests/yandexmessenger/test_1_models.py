import json

import pytest

from multibotkit.schemas.yandexmessenger.incoming import (
    Chat,
    ChatType,
    File,
    Image,
    Sender,
    Update,
)
from multibotkit.schemas.yandexmessenger.outgoing import (
    GetUpdatesParams,
    InlineKeyboard,
    InlineKeyboardButton,
    MessageResponse,
    SendFileParams,
    SendImageParams,
    SendTextParams,
    UpdatesResponse,
)


def test_incoming_models_sender():
    """Тест модели Sender"""
    # Sender с login (обычный пользователь)
    sender = Sender(login="test_user", display_name="Test User", robot=False)

    sender_json = sender.model_dump_json()
    sender_dict = json.loads(sender_json)

    assert sender_dict == {
        "login": "test_user",
        "display_name": "Test User",
        "robot": False,
        "id": None,
    }

    parsed_sender = Sender.model_validate(sender_dict)
    assert parsed_sender.login == "test_user"
    assert parsed_sender.display_name == "Test User"
    assert parsed_sender.robot is False

    # Sender с id (бот/канал)
    bot_sender = Sender(id="bot_12345", display_name="Bot Name", robot=True)

    bot_json = bot_sender.model_dump_json()
    bot_dict = json.loads(bot_json)

    assert bot_dict["id"] == "bot_12345"
    assert bot_dict["robot"] is True
    assert bot_dict["login"] is None


def test_incoming_models_chat():
    """Тест модели Chat"""
    # Private chat
    private_chat = Chat(type=ChatType.private)

    private_json = private_chat.model_dump_json()
    private_dict = json.loads(private_json)

    assert private_dict == {"type": "private", "id": None}

    # Group chat
    group_chat = Chat(type=ChatType.group, id="group_123")

    group_json = group_chat.model_dump_json()
    group_dict = json.loads(group_json)

    assert group_dict == {"type": "group", "id": "group_123"}

    parsed_chat = Chat.model_validate(group_dict)
    assert parsed_chat.type == ChatType.group
    assert parsed_chat.id == "group_123"


def test_incoming_models_image():
    """Тест модели Image"""
    image = Image(
        file_id="img_file_123", width=1920, height=1080, size=524288, name="photo.jpg"
    )

    image_json = image.model_dump_json()
    image_dict = json.loads(image_json)

    assert image_dict == {
        "file_id": "img_file_123",
        "width": 1920,
        "height": 1080,
        "size": 524288,
        "name": "photo.jpg",
    }

    parsed_image = Image.model_validate(image_dict)
    assert parsed_image.file_id == "img_file_123"
    assert parsed_image.width == 1920
    assert parsed_image.height == 1080


def test_incoming_models_file():
    """Тест модели File"""
    file = File(id="file_123", name="document.pdf", size=1048576)

    file_json = file.model_dump_json()
    file_dict = json.loads(file_json)

    assert file_dict == {"id": "file_123", "name": "document.pdf", "size": 1048576}

    parsed_file = File.model_validate(file_dict)
    assert parsed_file.id == "file_123"
    assert parsed_file.name == "document.pdf"
    assert parsed_file.size == 1048576


def test_incoming_models_update():
    """Тест модели Update (полное сообщение)"""
    sender_dict = {"login": "test_user", "display_name": "Test User"}

    chat_dict = {"type": "private"}

    image_dict = {"file_id": "img_123", "width": 800, "height": 600}

    update_dict = {
        "update_id": 12345,
        "message_id": 67890,
        "timestamp": 1706620800,
        "from": sender_dict,
        "chat": chat_dict,
        "text": "Hello from Yandex Messenger!",
        "images": [image_dict],
    }

    update = Update.model_validate(update_dict)

    assert update.update_id == 12345
    assert update.message_id == 67890
    assert update.timestamp == 1706620800
    assert update.from_.login == "test_user"
    assert update.chat.type == ChatType.private
    assert update.text == "Hello from Yandex Messenger!"
    assert len(update.images) == 1
    assert update.images[0].file_id == "img_123"

    # Сериализация обратно
    update_json = update.model_dump_json(by_alias=True)
    update_dict_parsed = json.loads(update_json)

    assert update_dict_parsed["update_id"] == 12345
    assert update_dict_parsed["from"]["login"] == "test_user"
    assert update_dict_parsed["text"] == "Hello from Yandex Messenger!"


def test_outgoing_models_inline_keyboard():
    """Тест модели InlineKeyboard"""
    button1 = InlineKeyboardButton(text="Button 1", callback_data={"action": "click1"})

    button2 = InlineKeyboardButton(text="Button 2", callback_data={"action": "click2"})

    keyboard = InlineKeyboard(buttons=[button1, button2])

    keyboard_json = keyboard.model_dump_json()
    keyboard_dict = json.loads(keyboard_json)

    assert keyboard_dict == {
        "buttons": [
            {"text": "Button 1", "callback_data": {"action": "click1"}},
            {"text": "Button 2", "callback_data": {"action": "click2"}},
        ]
    }

    parsed_keyboard = InlineKeyboard.model_validate(keyboard_dict)
    assert len(parsed_keyboard.buttons) == 2
    assert parsed_keyboard.buttons[0].text == "Button 1"


def test_outgoing_models_inline_keyboard_max_buttons():
    """Тест лимита 100 кнопок"""
    # Создаем 101 кнопку
    buttons = [
        InlineKeyboardButton(text=f"Button {i}", callback_data={"id": i})
        for i in range(101)
    ]

    with pytest.raises(ValueError, match="Максимум 100 кнопок"):
        InlineKeyboard(buttons=buttons)


def test_outgoing_models_send_text():
    """Тест модели SendTextParams"""
    params = SendTextParams(
        text="Test message",
        login="test_user",
        disable_notification=True,
        important=False,
    )

    params_json = params.model_dump_json()
    params_dict = json.loads(params_json)

    assert params_dict["text"] == "Test message"
    assert params_dict["login"] == "test_user"
    assert params_dict["disable_notification"] is True
    assert params_dict["important"] is False

    # Тест с chat_id вместо login
    group_params = SendTextParams(text="Group message", chat_id="group_123")

    group_dict = group_params.model_dump(exclude_none=True)
    assert group_dict["chat_id"] == "group_123"
    assert "login" not in group_dict


def test_outgoing_models_send_text_validation():
    """Тест валидации chat_id/login"""
    with pytest.raises(ValueError, match="Необходимо указать либо chat_id либо login"):
        SendTextParams(text="Test")


def test_outgoing_models_send_image():
    """Тест модели SendImageParams"""
    params = SendImageParams(login="test_user", thread_id=999)

    params_dict = params.model_dump(exclude_none=True)

    assert params_dict["login"] == "test_user"
    assert params_dict["thread_id"] == 999
    assert "chat_id" not in params_dict


def test_outgoing_models_send_image_validation():
    """Тест валидации chat_id/login для SendImageParams"""
    with pytest.raises(ValueError, match="Необходимо указать либо chat_id либо login"):
        SendImageParams()


def test_outgoing_models_send_file_validation():
    """Тест валидации chat_id/login для SendFileParams"""
    with pytest.raises(ValueError, match="Необходимо указать либо chat_id либо login"):
        SendFileParams()


def test_outgoing_models_get_updates():
    """Тест модели GetUpdatesParams"""
    params = GetUpdatesParams(limit=500, offset=100)

    params_dict = params.model_dump(exclude_none=True)

    assert params_dict["limit"] == 500
    assert params_dict["offset"] == 100


def test_outgoing_models_responses():
    """Тест моделей ответов от API"""
    # MessageResponse
    msg_response = MessageResponse(ok=True, message_id=12345)

    msg_json = msg_response.model_dump_json()
    msg_dict = json.loads(msg_json)

    assert msg_dict == {"ok": True, "message_id": 12345}

    # UpdatesResponse
    update_dict = {
        "update_id": 1,
        "message_id": 2,
        "timestamp": 1706620800,
        "from": {"login": "user"},
        "chat": {"type": "private"},
        "text": "test",
    }

    updates_response = UpdatesResponse(
        ok=True, updates=[Update.model_validate(update_dict)]
    )

    assert updates_response.ok is True
    assert len(updates_response.updates) == 1
    assert updates_response.updates[0].text == "test"
