import json

from multibotkit.schemas.telegram.incoming import (
    Location,
    Contact,
    Voice,
    Photo,
    MaskPosition,
    Sticker,
    VideoNote,
    Video,
    Document,
    Audio,
    Chat,
    User,
    Message as IncomingMessage,
    CallbackQuery,
    Update,
)
from multibotkit.schemas.telegram.outgoing import (
    SetWebhookParams,
    WebhookInfo,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Message as OutgoingMessage,
    InputMediaPhoto,
    InputMediaDocument,
    MediaGroup,
)


def test_incoming_models():

    location = Location(
        longitude=59.769595,
        latitude=30.796399,
        horizontal_accuracy=55.55,
        live_period=60,
        heading=180,
        proximity_alert_radius=10,
    )

    location_json = location.json()
    location_dict = json.loads(location_json)

    assert location_dict == {
        "longitude": 59.769595,
        "latitude": 30.796399,
        "horizontal_accuracy": 55.55,
        "live_period": 60,
        "heading": 180,
        "proximity_alert_radius": 10,
    }

    location = Location.parse_obj(location_dict)

    assert location.longitude == 59.769595
    assert location.latitude == 30.796399
    assert location.horizontal_accuracy == 55.55
    assert location.live_period == 60
    assert location.heading == 180
    assert location.proximity_alert_radius == 10

    contact = Contact(
        phone_number="89999999999",
        first_name="Name",
        last_name="Surname",
        user_id=1111,
        vcard="vcard",
    )

    contact_json = contact.json()
    contact_dict = json.loads(contact_json)

    assert contact_dict == {
        "phone_number": "89999999999",
        "first_name": "Name",
        "last_name": "Surname",
        "user_id": 1111,
        "vcard": "vcard",
    }

    contact = Contact.parse_obj(contact_dict)

    assert contact.phone_number == "89999999999"
    assert contact.first_name == "Name"
    assert contact.last_name == "Surname"
    assert contact.user_id == 1111
    assert contact.vcard == "vcard"

    voice = Voice(
        file_id="file id",
        file_unique_id="file unique id",
        file_size=512,
        duration=60,
        mime_type="MIME type",
    )

    voice_json = voice.json()
    voice_dict = json.loads(voice_json)

    assert voice_dict == {
        "file_id": "file id",
        "file_unique_id": "file unique id",
        "file_size": 512,
        "duration": 60,
        "mime_type": "MIME type",
    }

    voice = Voice.parse_obj(voice_dict)

    assert voice.file_id == "file id"
    assert voice.file_unique_id == "file unique id"
    assert voice.file_size == 512
    assert voice.duration == 60
    assert voice.mime_type == "MIME type"

    photo = Photo(
        file_id="file id",
        file_unique_id="file unique id",
        file_size=512,
        width=512,
        height=256,
    )

    photo_json = photo.json()
    photo_dict = json.loads(photo_json)

    assert photo_dict == {
        "file_id": "file id",
        "file_unique_id": "file unique id",
        "file_size": 512,
        "width": 512,
        "height": 256,
    }

    photo = Photo.parse_obj(photo_dict)

    assert photo.file_id == "file id"
    assert photo.file_unique_id == "file unique id"
    assert photo.file_size == 512
    assert photo.width == 512
    assert photo.height == 256

    mask_position = MaskPosition(point="eyes", x_shift=55.55, y_shift=55.55, scale=1.2)

    mask_position_json = mask_position.json()
    mask_position_dict = json.loads(mask_position_json)

    assert mask_position == {
        "point": "eyes",
        "x_shift": 55.55,
        "y_shift": 55.55,
        "scale": 1.2,
    }

    mask_position = MaskPosition.parse_obj(mask_position_dict)

    assert mask_position.point == "eyes"
    assert mask_position.x_shift == 55.55
    assert mask_position.y_shift == 55.55
    assert mask_position.scale == 1.2

    sticker = Sticker(
        file_id="file id",
        file_unique_id="file unique id",
        file_size=1024,
        width=256,
        height=512,
        is_animated=True,
        thumb=photo,
        emoji="😀",
        set_name="set name",
        mask_position=mask_position,
    )

    sticker_json = sticker.json()
    sticker_dict = json.loads(sticker_json)

    assert sticker_dict == {
        "file_id": "file id",
        "file_unique_id": "file unique id",
        "file_size": 1024,
        "width": 256,
        "height": 512,
        "is_animated": True,
        "thumb": photo_dict,
        "emoji": "😀",
        "set_name": "set name",
        "mask_position": mask_position_dict,
    }

    sticker = Sticker.parse_obj(sticker_dict)

    assert sticker.file_id == "file id"
    assert sticker.file_unique_id == "file unique id"
    assert sticker.file_size == 1024
    assert sticker.width == 256
    assert sticker.height == 512
    assert sticker.is_animated == True
    assert sticker.thumb == photo
    assert sticker.emoji == "😀"
    assert sticker.set_name == "set name"
    assert sticker.mask_position == mask_position

    video_note = VideoNote(
        file_id="file id",
        file_unique_id="file unique id",
        file_size=512,
        length=128,
        duration=60,
        thumb=photo,
    )

    video_note_json = video_note.json()
    video_note_dict = json.loads(video_note_json)

    assert video_note_dict == {
        "file_id": "file id",
        "file_unique_id": "file unique id",
        "file_size": 512,
        "length": 128,
        "duration": 60,
        "thumb": photo_dict,
    }

    video_note = VideoNote.parse_obj(video_note_dict)

    assert video_note.file_id == "file id"
    assert video_note.file_unique_id == "file unique id"
    assert video_note.file_size == 512
    assert video_note.length == 128
    assert video_note.duration == 60
    assert video_note.thumb == photo

    video = Video(
        file_id="file id",
        file_unique_id="file unique id",
        file_size=512,
        width=256,
        height=128,
        duration=60,
        thumb=photo,
        file_name="video.flv",
        mime_type="MIME type",
    )

    video_json = video.json()
    video_dict = json.loads(video_json)

    assert video_dict == {
        "file_id": "file id",
        "file_unique_id": "file unique id",
        "file_size": 512,
        "width": 256,
        "height": 128,
        "duration": 60,
        "thumb": photo_dict,
        "file_name": "video.flv",
        "mime_type": "MIME type",
    }

    video = Video.parse_obj(video_dict)

    assert video.file_id == "file id"
    assert video.file_unique_id == "file unique id"
    assert video.file_size == 512
    assert video.width == 256
    assert video.height == 128
    assert video.duration == 60
    assert video.thumb == photo
    assert video.file_name == "video.flv"
    assert video.mime_type == "MIME type"

    document = Document(
        file_id="file id",
        file_unique_id="file unique id",
        file_size=512,
        thumb=photo,
        file_name="document.doc",
        mime_type="MIME type",
    )

    document_json = document.json()
    document_dict = json.loads(document_json)

    assert document_dict == {
        "file_id": "file id",
        "file_unique_id": "file unique id",
        "file_size": 512,
        "thumb": photo_dict,
        "file_name": "document.doc",
        "mime_type": "MIME type",
    }

    document = Document.parse_obj(document_dict)

    assert document.file_id == "file id"
    assert document.file_unique_id == "file unique id"
    assert document.file_size == 512
    assert document.thumb == photo
    assert document.file_name == "document.doc"
    assert document.mime_type == "MIME type"

    audio = Audio(
        file_id="file id",
        file_unique_id="file unique id",
        file_size=512,
        duration=60,
        performer="perfomer",
        title="title",
        file_name="audio.mp3",
        mime_type="MIME type",
        thumb=photo,
    )

    audio_json = audio.json()
    audio_dict = json.loads(audio_json)

    assert audio_dict == {
        "file_id": "file id",
        "file_unique_id": "file unique id",
        "file_size": 512,
        "duration": 60,
        "performer": "perfomer",
        "title": "title",
        "file_name": "audio.mp3",
        "mime_type": "MIME type",
        "thumb": photo_dict,
    }

    audio = Audio.parse_obj(audio_dict)

    assert audio.file_id == "file id"
    assert audio.file_unique_id == "file unique id"
    assert audio.file_size == 512
    assert audio.duration == 60
    assert audio.performer == "perfomer"
    assert audio.title == "title"
    assert audio.file_name == "audio.mp3"
    assert audio.mime_type == "MIME type"
    assert audio.thumb == photo

    chat = Chat(
        id=1234,
        type="group",
        title="title",
        first_name="Name",
        last_name="Surname",
        username="username",
    )

    chat_json = chat.json()
    chat_dict = json.loads(chat_json)

    assert chat_dict == {
        "id": 1234,
        "type": "group",
        "title": "title",
        "first_name": "Name",
        "last_name": "Surname",
        "username": "username",
    }

    chat = Chat.parse_obj(chat_dict)

    assert chat == Chat(
        id=1234,
        type="group",
        title="title",
        first_name="Name",
        last_name="Surname",
        username="username",
    )

    user = User(
        id=1234,
        is_bot=False,
        first_name="Name",
        last_name="Surname",
        username="username",
        language_code="ru",
        can_join_groups=True,
        can_read_all_group_messages=True,
        supports_inline_queries=True,
    )

    user_json = user.json()
    user_dict = json.loads(user_json)

    assert user_dict == {
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

    user = User.parse_obj(user_dict)

    assert user == User(
        id=1234,
        is_bot=False,
        first_name="Name",
        last_name="Surname",
        username="username",
        language_code="ru",
        can_join_groups=True,
        can_read_all_group_messages=True,
        supports_inline_queries=True,
    )

    message_dict = {
        "message_id": 1234,
        "date": 1656425873,
        "from": user_dict,
        "chat": chat_dict,
        "text": "text",
        "caption": "Caption",
        "audio": audio_dict,
        "document": document_dict,
        "photo": [photo_dict, photo_dict],
        "sticker": sticker_dict,
        "video": video_dict,
        "video_note": video_note_dict,
        "voice": voice_dict,
        "contact": contact_dict,
        "location": location_dict,
    }

    callback_query_dict = {
        "id": "callback query id",
        "from": user_dict,
        "message": message_dict,
        "inline_message_id": 1234,
        "chat_instance": "chat instance",
        "data": "data",
        "game_short_name": "game short name",
    }

    message = IncomingMessage.parse_obj(message_dict)

    assert message.message_id == 1234
    assert message.date == 1656425873
    assert message.from_ == user
    assert message.chat == chat
    assert message.text == "text"
    assert message.caption == "Caption"
    assert message.audio == audio
    assert message.document == document
    assert message.photo == [photo, photo]
    assert message.sticker == sticker
    assert message.video == video
    assert message.video_note == video_note
    assert message.voice == voice
    assert message.contact == contact
    assert message.location == location

    message_json = message.json()
    message_dict = json.loads(message_json)

    assert message_dict == {
        "message_id": 1234,
        "date": 1656425873,
        "from_": user_dict,
        "chat": chat_dict,
        "text": "text",
        "caption": "Caption",
        "audio": audio_dict,
        "document": document_dict,
        "photo": [photo_dict, photo_dict],
        "sticker": sticker_dict,
        "video": video_dict,
        "video_note": video_note_dict,
        "voice": voice_dict,
        "contact": contact_dict,
        "location": location_dict,
    }

    callback_query = CallbackQuery.parse_obj(callback_query_dict)

    assert callback_query.id == "callback query id"
    assert callback_query.from_ == user
    assert callback_query.message == message
    assert callback_query.inline_message_id == 1234
    assert callback_query.chat_instance == "chat instance"
    assert callback_query.data == "data"
    assert callback_query.game_short_name == "game short name"

    callback_query_json = callback_query.json()
    callback_query_dict = json.loads(callback_query_json)

    assert callback_query_dict == {
        "id": "callback query id",
        "from_": user_dict,
        "message": message_dict,
        "inline_message_id": 1234,
        "chat_instance": "chat instance",
        "data": "data",
        "game_short_name": "game short name",
    }

    update = Update(
        update_id=1234,
        message=message,
        edited_message=message,
        callback_query=callback_query,
    )

    update_json = update.json()
    update_dict = json.loads(update_json)

    assert update_dict == {
        "update_id": 1234,
        "message": message_dict,
        "edited_message": message_dict,
        "callback_query": callback_query_dict,
    }

    message_dict = {
        "message_id": 1234,
        "date": 1656425873,
        "from": user_dict,
        "chat": chat_dict,
        "text": "text",
        "caption": "Caption",
        "audio": audio_dict,
        "document": document_dict,
        "photo": [photo_dict, photo_dict],
        "sticker": sticker_dict,
        "video": video_dict,
        "video_note": video_note_dict,
        "voice": voice_dict,
        "contact": contact_dict,
        "location": location_dict,
    }

    callback_query_dict = {
        "id": "callback query id",
        "from": user_dict,
        "message": message_dict,
        "inline_message_id": 1234,
        "chat_instance": "chat instance",
        "data": "data",
        "game_short_name": "game short name",
    }

    update_dict = {
        "update_id": 1234,
        "message": message_dict,
        "edited_message": message_dict,
        "callback_query": callback_query_dict,
    }

    update = Update.parse_obj(update_dict)

    assert update == Update(
        update_id=1234,
        message=message,
        edited_message=message,
        callback_query=callback_query,
    )


def test_outgoing_models():

    set_webhook_params = SetWebhookParams(
        url="https://url.com",
        ip_address="111.111.111.111",
        max_connections=10,
        allowed_updates=["message", "edited_channel_post", "callback_query"],
    )

    set_webhook_params_json = set_webhook_params.json()
    set_webhook_params_dict = json.loads(set_webhook_params_json)

    assert set_webhook_params_dict == {
        "url": "https://url.com",
        "ip_address": "111.111.111.111",
        "max_connections": 10,
        "allowed_updates": ["message", "edited_channel_post", "callback_query"],
    }

    set_webhook_params = SetWebhookParams.parse_obj(set_webhook_params_dict)

    assert set_webhook_params == SetWebhookParams(
        url="https://url.com",
        ip_address="111.111.111.111",
        max_connections=10,
        allowed_updates=["message", "edited_channel_post", "callback_query"],
    )

    webhook_info = WebhookInfo(
        url="https://url.com",
        has_custom_certificate=False,
        pending_update_count=2,
        ip_address="111.111.111.111",
        last_error_date=1656425873,
        last_error_message="error message",
        max_connections=10,
        allowed_updates=["message", "edited_channel_post", "callback_query"],
    )

    webhook_info_json = webhook_info.json()
    webhook_info_dict = json.loads(webhook_info_json)

    assert webhook_info_dict == {
        "url": "https://url.com",
        "has_custom_certificate": False,
        "pending_update_count": 2,
        "ip_address": "111.111.111.111",
        "last_error_date": 1656425873,
        "last_error_message": "error message",
        "max_connections": 10,
        "allowed_updates": ["message", "edited_channel_post", "callback_query"],
    }

    webhook_info = WebhookInfo.parse_obj(webhook_info_dict)

    assert webhook_info == WebhookInfo(
        url="https://url.com",
        has_custom_certificate=False,
        pending_update_count=2,
        ip_address="111.111.111.111",
        last_error_date=1656425873,
        last_error_message="error message",
        max_connections=10,
        allowed_updates=["message", "edited_channel_post", "callback_query"],
    )

    inline_keyboard_button = InlineKeyboardButton(
        text="Button", url="https://url.com", callback_data="callback data"
    )

    inline_keyboard_button_json = inline_keyboard_button.json()
    inline_keyboard_button_dict = json.loads(inline_keyboard_button_json)

    assert inline_keyboard_button_dict == {
        "text": "Button",
        "url": "https://url.com",
        "callback_data": "callback data",
    }

    inline_keyboard_button = InlineKeyboardButton.parse_obj(inline_keyboard_button_dict)

    assert inline_keyboard_button == InlineKeyboardButton(
        text="Button", url="https://url.com", callback_data="callback data"
    )

    inline_keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_keyboard_button, inline_keyboard_button]]
    )

    inline_keyboard_markup_json = inline_keyboard_markup.json()
    inline_keyboard_markup_dict = json.loads(inline_keyboard_markup_json)

    assert inline_keyboard_markup_dict == {
        "inline_keyboard": [[inline_keyboard_button_dict, inline_keyboard_button_dict]]
    }

    inline_keyboard_markup = InlineKeyboardMarkup.parse_obj(inline_keyboard_markup_dict)

    assert inline_keyboard_markup == InlineKeyboardMarkup(
        inline_keyboard=[[inline_keyboard_button, inline_keyboard_button]]
    )

    keyboard_button = KeyboardButton(
        text="Button", request_contact=False, request_location=False
    )

    keyboard_button_json = keyboard_button.json()
    keyboard_button_dict = json.loads(keyboard_button_json)

    assert keyboard_button_dict == {
        "text": "Button",
        "request_contact": False,
        "request_location": False,
    }

    keyboard_button = KeyboardButton.parse_obj(keyboard_button_dict)

    reply_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False,
    )

    reply_keyboard_markup_json = reply_keyboard_markup.json()
    reply_keyboard_markup_dict = json.loads(reply_keyboard_markup_json)

    assert reply_keyboard_markup_dict == {
        "keyboard": [[keyboard_button_dict, keyboard_button_dict]],
        "resize_keyboard": False,
        "one_time_keyboard": False,
    }

    reply_keyboard_markup = ReplyKeyboardMarkup.parse_obj(reply_keyboard_markup_dict)

    assert reply_keyboard_markup == ReplyKeyboardMarkup(
        keyboard=[[keyboard_button, keyboard_button]],
        resize_keyboard=False,
        one_time_keyboard=False,
    )

    message = OutgoingMessage(
        chat_id=1234,
        text="text",
        disable_web_page_preview=False,
        reply_markup=reply_keyboard_markup,
    )

    message_json = message.json()
    message_dict = json.loads(message_json)

    assert message_dict == {
        "chat_id": 1234,
        "text": "text",
        "disable_web_page_preview": False,
        "reply_markup": reply_keyboard_markup_dict,
    }

    message = OutgoingMessage.parse_obj(message_dict)

    assert message == OutgoingMessage(
        chat_id=1234,
        text="text",
        disable_web_page_preview=False,
        reply_markup=reply_keyboard_markup,
    )

    input_media_photo = InputMediaPhoto(
        type="photo", media="media", caption="caption", parse_mode="parse mode"
    )

    input_media_photo_json = input_media_photo.json()
    input_media_photo_dict = json.loads(input_media_photo_json)

    assert input_media_photo_dict == {
        "type": "photo",
        "media": "media",
        "caption": "caption",
        "parse_mode": "parse mode",
    }

    input_media_photo = InputMediaPhoto.parse_obj(input_media_photo_dict)

    assert input_media_photo == InputMediaPhoto(
        type="photo", media="media", caption="caption", parse_mode="parse mode"
    )

    input_media_document = InputMediaDocument(
        type="photo",
        media=["media1", "media2"],
        caption="caption",
        parse_mode="parse mode",
    )

    input_media_document_json = input_media_document.json()
    input_media_document_dict = json.loads(input_media_document_json)

    assert input_media_document_dict == {
        "type": "photo",
        "media": ["media1", "media2"],
        "caption": "caption",
        "parse_mode": "parse mode",
    }

    input_media_document = InputMediaDocument.parse_obj(input_media_document_dict)

    assert input_media_document == InputMediaDocument(
        type="photo",
        media=["media1", "media2"],
        caption="caption",
        parse_mode="parse mode",
    )

    media_group = MediaGroup(chat_id=1234, media=[input_media_photo, input_media_photo])

    media_group_json = media_group.json()
    media_group_dict = json.loads(media_group_json)

    assert media_group_dict == {
        "chat_id": 1234,
        "media": [input_media_photo_dict, input_media_photo_dict],
    }

    media_group = MediaGroup.parse_obj(media_group_dict)

    assert media_group == MediaGroup(
        chat_id=1234, media=[input_media_photo, input_media_photo]
    )
