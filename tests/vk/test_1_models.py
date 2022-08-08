import json

from multibotkit.schemas.vk.incoming import (
    ClientInfo,
    CoordinatesObject,
    GeoObject,
    MessageObject,
    EventObject,
    IncomingEvent,
)
from multibotkit.schemas.vk.outgoing import (
    KeyboardAction,
    KeyboardButton,
    Keyboard,
    Message,
    Element,
    Template,
)


def test_icoming_models():

    client_info = ClientInfo(
        button_actions=[],
        carousel=False,
        inline_keyboard=False,
        keyboard=False,
        lang_id=1234,
    )

    client_info_json = client_info.json()
    client_info_dict = json.loads(client_info_json)

    assert client_info_dict == {
        "button_actions": [],
        "carousel": False,
        "inline_keyboard": False,
        "keyboard": False,
        "lang_id": 1234,
    }

    client_info = ClientInfo.parse_obj(client_info_dict)

    assert client_info == ClientInfo(
        button_actions=[],
        carousel=False,
        inline_keyboard=False,
        keyboard=False,
        lang_id=1234,
    )

    coordinates_object = CoordinatesObject(longitude=59.769595, latitude=30.796399)

    coordinates_object_json = coordinates_object.json()
    coordinates_object_dict = json.loads(coordinates_object_json)

    assert coordinates_object_dict == {"longitude": 59.769595, "latitude": 30.796399}

    coordinates_object = CoordinatesObject.parse_obj(coordinates_object_dict)

    assert coordinates_object == CoordinatesObject(
        longitude=59.769595, latitude=30.796399
    )

    geo_object = GeoObject(type="geo object type", coordinates=coordinates_object)

    geo_object_json = geo_object.json()
    geo_object_dict = json.loads(geo_object_json)

    assert geo_object_dict == {
        "type": "geo object type",
        "coordinates": coordinates_object_dict,
    }

    geo_object = GeoObject.parse_obj(geo_object_dict)

    assert geo_object == GeoObject(
        type="geo object type", coordinates=coordinates_object
    )

    message_object = MessageObject(
        attachments=[],
        conversation_message_id=1234,
        date=1656425873,
        from_id="from id",
        peer_id="peer id",
        random_id=1111,
        fwd_messages=[],
        ref="ref",
        id=2222,
        out=3333,
        important=False,
        is_hidden=False,
        text="text",
        payload="payload",
        geo=geo_object,
    )

    message_object_json = message_object.json()
    message_object_dict = json.loads(message_object_json)

    assert message_object_dict == {
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

    message_object = MessageObject.parse_obj(message_object_dict)

    assert message_object == MessageObject(
        attachments=[],
        conversation_message_id=1234,
        date=1656425873,
        from_id="from id",
        peer_id="peer id",
        random_id=1111,
        fwd_messages=[],
        ref="ref",
        id=2222,
        out=3333,
        important=False,
        is_hidden=False,
        text="text",
        payload="payload",
        geo=geo_object,
    )

    event_object = EventObject(client_info=client_info, message=message_object)

    event_object_json = event_object.json()
    event_object_dict = json.loads(event_object_json)

    assert event_object_dict == {
        "client_info": client_info_dict,
        "message": message_object_dict,
    }

    event_object = EventObject.parse_obj(event_object_dict)

    assert event_object == EventObject(client_info=client_info, message=message_object)

    incoming_event = IncomingEvent(
        type="event type", group_id=1234, object=event_object
    )

    incoming_event_json = incoming_event.json()
    incoming_event_dict = json.loads(incoming_event_json)

    assert incoming_event_dict == {
        "type": "event type",
        "group_id": 1234,
        "object": event_object_dict,
    }

    incoming_event = IncomingEvent.parse_obj(incoming_event_dict)

    assert incoming_event == IncomingEvent(
        type="event type", group_id=1234, object=event_object
    )


def test_outgoing_models():

    keyboard_action = KeyboardAction(type="type", label="label", payload="payload")

    keyboard_action_json = keyboard_action.json()
    keyboard_action_dict = json.loads(keyboard_action_json)

    assert keyboard_action_dict == {
        "type": "type",
        "label": "label",
        "payload": "payload",
    }

    keyboard_action = KeyboardAction.parse_obj(keyboard_action_dict)

    assert keyboard_action == KeyboardAction(
        type="type", label="label", payload="payload"
    )

    keyboard_button = KeyboardButton(action=keyboard_action, color="color")

    keyboard_button_json = keyboard_button.json()
    keyboard_button_dict = json.loads(keyboard_button_json)

    assert keyboard_button_dict == {"action": keyboard_action_dict, "color": "color"}

    keyboard_button = KeyboardButton.parse_obj(keyboard_button_dict)

    assert keyboard_button == KeyboardButton(action=keyboard_action, color="color")

    keyboard = Keyboard(one_time=False, inline=True, buttons=[[keyboard_button]])

    keyboard_json = keyboard.json()
    keyboard_dict = json.loads(keyboard_json)

    assert keyboard_dict == {
        "one_time": False,
        "inline": True,
        "buttons": [[keyboard_button_dict]],
    }

    keyboard = Keyboard.parse_obj(keyboard_dict)

    assert keyboard == Keyboard(
        one_time=False, inline=True, buttons=[[keyboard_button]]
    )

    message = Message(
        user_id=1234,
        message="message",
        keyboard=keyboard,
        lat=0,
        long=0,
        attachment="attachment",
        template={},
    )

    message_json = message.json()
    message_dict = json.loads(message_json)

    assert message_dict == {
        "user_id": 1234,
        "message": "message",
        "keyboard": keyboard_dict,
        "lat": 0,
        "long": 0,
        "attachment": "attachment",
        "template": {},
    }

    message = Message.parse_obj(message_dict)

    assert message == Message(
        user_id=1234,
        message="message",
        keyboard=keyboard,
        lat=0,
        long=0,
        attachment="attachment",
        template={},
    )

    element = Element(
        title="title",
        description="desription",
        photo_id="photo id",
        buttons=[keyboard_button],
        action={},
    )

    element_json = element.json()
    element_dict = json.loads(element_json)

    assert element_dict == {
        "title": "title",
        "description": "desription",
        "photo_id": "photo id",
        "buttons": [keyboard_button_dict],
        "action": {},
    }

    element = Element.parse_obj(element_dict)

    assert element == Element(
        title="title",
        description="desription",
        photo_id="photo id",
        buttons=[keyboard_button],
        action={},
    )

    template = Template(type="type", elements=[element])

    template_json = template.json()
    template_dict = json.loads(template_json)

    assert template_dict == {"type": "type", "elements": [element_dict]}

    template = Template.parse_obj(template_dict)

    assert template == Template(type="type", elements=[element])
