import json

from multibotkit.schemas.viber.incoming import (
    Location as IncomingLocation,
    Contact as IncomingContact,
    Message,
    User,
    ReceivingMessageCallback,
    SubscriptionCallback,
    UnsubscribeCallback,
    ConversationStartedCallback,
    FailedCallback,
    Callback,
)
from multibotkit.schemas.viber.outgoing import (
    Button,
    Keyboard,
    SetWebhook,
    Sender,
    Contact as OutgoingContact,
    Location as OutgoingLocation,
    BaseMessage,
    TextMessage,
    PictureMessage,
    VideoMessage,
    FileMessage,
    ContactMessage,
    LocationMessage,
    UrlMessage,
    StickerMessage,
)


def test_viber_incoming_models():

    location = IncomingLocation(lat="+90°", lon="-180°")

    location_dict = json.loads(location.model_dump_json())

    assert location_dict == {"lat": "+90°", "lon": "-180°"}

    location = IncomingLocation.model_validate(location_dict)

    assert location == IncomingLocation(lat="+90°", lon="-180°")

    contact = IncomingContact(name="Name", phone_number="89999999999", avatar="avatar")

    contact_dict = json.loads(contact.model_dump_json())

    assert contact_dict == {
        "name": "Name",
        "phone_number": "89999999999",
        "avatar": "avatar",
    }

    contact = IncomingContact.model_validate(contact_dict)

    assert contact == IncomingContact(
        name="Name", phone_number="89999999999", avatar="avatar"
    )

    message = Message(
        type="text",
        text="text",
        media="media",
        location=location,
        contact=contact,
        tracking_data="tracking data",
        file_name="file name",
        file_size=512,
        duration=60,
        sticker_id=1234,
    )

    message_dict = json.loads(message.model_dump_json())

    assert message_dict == {
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

    message = Message.model_validate(message_dict)

    assert message == Message(
        type="text",
        text="text",
        media="media",
        location=location,
        contact=contact,
        tracking_data="tracking data",
        file_name="file name",
        file_size=512,
        duration=60,
        sticker_id=1234,
    )

    user = User(
        id="user id",
        name="Name",
        avatar="avatar",
        country="RU",
        language="ru",
        api_version=1111,
    )

    user_dict = json.loads(user.model_dump_json())

    assert user_dict == {
        "id": "user id",
        "name": "Name",
        "avatar": "avatar",
        "country": "RU",
        "language": "ru",
        "api_version": 1111,
    }

    user = User.model_validate(user_dict)

    assert user == User(
        id="user id",
        name="Name",
        avatar="avatar",
        country="RU",
        language="ru",
        api_version=1111,
    )

    receiving_message_callback = ReceivingMessageCallback(sender=user, message=message)

    receiving_message_callback_dict = json.loads(receiving_message_callback.model_dump_json())

    assert receiving_message_callback_dict == {
        "sender": user_dict,
        "message": message_dict,
    }

    receiving_message_callback = ReceivingMessageCallback.model_validate(
        receiving_message_callback_dict
    )

    assert receiving_message_callback == ReceivingMessageCallback(
        sender=user, message=message
    )

    subscription_callback = SubscriptionCallback(user=user)

    subscription_callback_dict = json.loads(subscription_callback.model_dump_json())

    assert subscription_callback_dict == {"user": user_dict}

    subscription_callback = SubscriptionCallback.model_validate(subscription_callback_dict)

    assert subscription_callback == SubscriptionCallback(user=user)

    unsubscribe_callback = UnsubscribeCallback(user_id="user id")

    unsubscribe_callback_dict = json.loads(unsubscribe_callback.model_dump_json())

    assert unsubscribe_callback_dict == {"user_id": "user id"}

    unsubscribe_callback = UnsubscribeCallback.model_validate(unsubscribe_callback_dict)

    assert unsubscribe_callback == UnsubscribeCallback(user_id="user id")

    conversation_started_callback = ConversationStartedCallback(
        type="type", context="context", user=user, subscribed=False
    )

    conversation_started_callback_dict = json.loads(
        conversation_started_callback.model_dump_json()
    )

    assert conversation_started_callback_dict == {
        "type": "type",
        "context": "context",
        "user": user_dict,
        "subscribed": False,
    }

    conversation_started_callback = ConversationStartedCallback.model_validate(
        conversation_started_callback_dict
    )

    assert conversation_started_callback == ConversationStartedCallback(
        type="type", context="context", user=user, subscribed=False
    )

    failed_callback = FailedCallback(user_id="user id", desc="desc")

    failed_callback_dict = json.loads(failed_callback.model_dump_json())

    assert failed_callback_dict == {"user_id": "user id", "desc": "desc"}

    failed_callback = FailedCallback.model_validate(failed_callback_dict)

    assert failed_callback == FailedCallback(user_id="user id", desc="desc")

    callback = Callback(
        user_id="user id",
        desc="desc",
        type="type",
        context="context",
        user=user,
        subscribed=False,
        sender=user,
        message=message,
        event="event",
        timestamp=6000000,
        message_token=1234,
    )

    callback_dict = json.loads(callback.model_dump_json())

    assert callback_dict == {
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

    callback = Callback.model_validate(callback_dict)

    assert callback == Callback(
        user_id="user id",
        desc="desc",
        type="type",
        context="context",
        user=user,
        subscribed=False,
        sender=user,
        message=message,
        event="event",
        timestamp=6000000,
        message_token=1234,
    )


def test_viber_outgoing_models():

    button = Button(
        Columns=1,
        Rows=1,
        Text="text",
        TextSize="10",
        TextHAlign="text H align",
        TextVAlign="text V align",
        ActionType="action type",
        ActionBody="action body",
        BgColor="bg color",
        Image="image",
    )

    button_dict = json.loads(button.model_dump_json())

    assert button_dict == {
        "Columns": 1,
        "Rows": 1,
        "Text": "text",
        "TextSize": "10",
        "TextHAlign": "text H align",
        "TextVAlign": "text V align",
        "ActionType": "action type",
        "ActionBody": "action body",
        "BgColor": "bg color",
        "Image": "image",
    }

    button = Button.model_validate(button_dict)

    assert button == Button(
        Columns=1,
        Rows=1,
        Text="text",
        TextSize="10",
        TextHAlign="text H align",
        TextVAlign="text V align",
        ActionType="action type",
        ActionBody="action body",
        BgColor="bg color",
        Image="image",
    )

    keyboard = Keyboard(
        Type="type", DefaultHeight=True, BgColor="bg color", Buttons=[button]
    )

    keyboard_dict = json.loads(keyboard.model_dump_json())

    assert keyboard_dict == {
        "Type": "type",
        "DefaultHeight": True,
        "BgColor": "bg color",
        "Buttons": [button_dict],
    }

    keyboard = Keyboard.model_validate(keyboard_dict)

    assert keyboard == Keyboard(
        Type="type", DefaultHeight=True, BgColor="bg color", Buttons=[button]
    )

    set_webhook = SetWebhook(
        url="url", event_types=["event_type"], send_name=True, send_photo=False
    )

    set_webhook_dict = json.loads(set_webhook.model_dump_json())

    assert set_webhook_dict == {
        "url": "url",
        "event_types": ["event_type"],
        "send_name": True,
        "send_photo": False,
    }

    set_webhook = SetWebhook.model_validate(set_webhook_dict)

    assert set_webhook == SetWebhook(
        url="url", event_types=["event_type"], send_name=True, send_photo=False
    )

    sender = Sender(name="name", avatar="avatar")

    sender_dict = json.loads(sender.model_dump_json())

    assert sender_dict == {"name": "name", "avatar": "avatar"}

    sender = Sender.model_validate(sender_dict)

    assert sender == Sender(name="name", avatar="avatar")

    contact = OutgoingContact(name="Name", phone_number="89999999999")

    contact_dict = json.loads(contact.model_dump_json())

    assert contact_dict == {"name": "Name", "phone_number": "89999999999"}

    contact = OutgoingContact.model_validate(contact_dict)

    assert contact == OutgoingContact(name="Name", phone_number="89999999999")

    location = OutgoingLocation(lat="+90°", lon="-180°")

    location_dict = json.loads(location.model_dump_json())

    assert location_dict == {"lat": "+90°", "lon": "-180°"}

    location = OutgoingLocation.model_validate(location_dict)

    assert location == OutgoingLocation(lat="+90°", lon="-180°")

    base_message = BaseMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
    )

    base_message_dict = json.loads(base_message.model_dump_json())

    assert base_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
    }

    base_message = BaseMessage.model_validate(base_message_dict)

    assert base_message == BaseMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
    )

    text_message = TextMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="text",
        text="text",
    )

    text_message_dict = json.loads(text_message.model_dump_json())

    assert text_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
        "type": "text",
        "text": "text",
    }

    text_message = TextMessage.model_validate(text_message_dict)

    assert text_message == TextMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="text",
        text="text",
    )

    picture_message = PictureMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="picture",
        text="text",
        media="media",
        thumbnail="thumbnail",
    )

    picture_message_dict = json.loads(picture_message.model_dump_json())

    assert picture_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
        "type": "picture",
        "text": "text",
        "media": "media",
        "thumbnail": "thumbnail",
    }

    picture_message = PictureMessage.model_validate(picture_message_dict)

    assert picture_message == PictureMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="picture",
        text="text",
        media="media",
        thumbnail="thumbnail",
    )

    video_message = VideoMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="video",
        media="media",
        thumbnail="thumbnail",
        size=512,
        duration=60,
    )

    video_message_dict = json.loads(video_message.model_dump_json())

    assert video_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
        "type": "video",
        "media": "media",
        "thumbnail": "thumbnail",
        "size": 512,
        "duration": 60,
    }

    video_message = VideoMessage.model_validate(video_message_dict)

    assert video_message == VideoMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="video",
        media="media",
        thumbnail="thumbnail",
        size=512,
        duration=60,
    )

    file_message = FileMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="file",
        media="media",
        size=512,
        file_name="file name",
    )

    file_message_dict = json.loads(file_message.model_dump_json())

    assert file_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
        "type": "file",
        "media": "media",
        "size": 512,
        "file_name": "file name",
    }

    file_message = FileMessage.model_validate(file_message_dict)

    assert file_message == FileMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="file",
        media="media",
        size=512,
        file_name="file name",
    )

    contact_message = ContactMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="contact",
        contact=contact,
    )

    contact_message_dict = json.loads(contact_message.model_dump_json())

    assert contact_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
        "type": "contact",
        "contact": contact_dict,
    }

    contact_message = ContactMessage.model_validate(contact_message_dict)

    assert contact_message == ContactMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="contact",
        contact=contact,
    )

    location_message = LocationMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="location",
        location=location,
    )

    location_message_dict = json.loads(location_message.model_dump_json())

    assert location_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
        "type": "location",
        "location": location_dict,
    }

    location_message = LocationMessage.model_validate(location_message_dict)

    assert location_message == LocationMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="location",
        location=location,
    )

    url_message = UrlMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="url",
        media="media",
    )

    url_message_dict = json.loads(url_message.model_dump_json())

    assert url_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
        "type": "url",
        "media": "media",
    }

    sticker_message = StickerMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="sticker",
        sticker_id=1234,
    )

    sticker_message_dict = json.loads(sticker_message.model_dump_json())

    assert sticker_message_dict == {
        "receiver": "reciever",
        "min_api_version": 1111,
        "sender": sender_dict,
        "tracking_data": "tracking data",
        "keyboard": keyboard_dict,
        "type": "sticker",
        "sticker_id": 1234,
    }

    sticker_message = StickerMessage.model_validate(sticker_message_dict)

    assert sticker_message == StickerMessage(
        receiver="reciever",
        min_api_version=1111,
        sender=sender,
        tracking_data="tracking data",
        keyboard=keyboard,
        type="sticker",
        sticker_id=1234,
    )
