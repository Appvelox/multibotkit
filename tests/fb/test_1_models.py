import json

from multibotkit.schemas.fb.incoming_messages import (
    EventEntryMessageRecipient,
    EventEntryMessageSender,
    MessageAttachmentPayload,
    MessageAttachment,
    ReferralData,
    MessagePostback,
    EventEntryMessageData,
    EventEntryMessage,
    EventEntry,
    IncomingEvent,
)
from multibotkit.schemas.fb.outgoing_messages import (
    GenericTemplateButton,
    GenericTemplateElement,
    QuickReply,
    MessageDataAttachmentPayload,
    MessageDataAttachment,
    MessageData,
    MessageRecipient,
    Message,
)


def test_fb_incoming_models():

    event_entry_message_recipient = EventEntryMessageRecipient(id="id")

    event_entry_message_recipient_dict = json.loads(
        event_entry_message_recipient.json()
    )

    assert event_entry_message_recipient_dict == {"id": "id"}

    event_entry_message_recipient = EventEntryMessageRecipient.parse_obj(
        event_entry_message_recipient_dict
    )
    assert event_entry_message_recipient == EventEntryMessageRecipient(id="id")

    event_entry_message_sender = EventEntryMessageSender(id="id")

    event_entry_message_sender_dict = json.loads(event_entry_message_sender.json())

    assert event_entry_message_sender_dict == {"id": "id"}

    event_entry_message_sender = EventEntryMessageSender.parse_obj(
        event_entry_message_sender_dict
    )

    assert event_entry_message_sender == EventEntryMessageSender(id="id")

    message_attachment_payload = MessageAttachmentPayload(url="url")

    message_attachment_payload_dict = json.loads(message_attachment_payload.json())

    assert message_attachment_payload_dict == {"url": "url"}

    message_attachment_payload = MessageAttachmentPayload.parse_obj(
        message_attachment_payload_dict
    )

    assert message_attachment_payload == MessageAttachmentPayload(url="url")

    message_attachment = MessageAttachment(
        type="type", payload=message_attachment_payload
    )

    message_attachment_dict = json.loads(message_attachment.json())

    assert message_attachment_dict == {
        "type": "type",
        "payload": message_attachment_payload_dict,
    }

    message_attachment = MessageAttachment.parse_obj(message_attachment_dict)

    assert message_attachment == MessageAttachment(
        type="type", payload=message_attachment_payload
    )

    referral_data = ReferralData(ref="ref", source="source", type="type")

    referral_data_dict = json.loads(referral_data.json())

    assert referral_data_dict == {"ref": "ref", "source": "source", "type": "type"}

    referral_data = ReferralData.parse_obj(referral_data_dict)

    assert referral_data == ReferralData(ref="ref", source="source", type="type")

    message_postback = MessagePostback(
        title="title", payload="payload", referral=referral_data
    )

    message_postback_dict = json.loads(message_postback.json())

    assert message_postback_dict == {
        "title": "title",
        "payload": "payload",
        "referral": referral_data_dict,
    }

    message_postback = MessagePostback.parse_obj(message_postback_dict)

    assert message_postback == MessagePostback(
        title="title", payload="payload", referral=referral_data
    )

    event_entry_message_data = EventEntryMessageData(
        mid="mid", text="text", attachments=[message_attachment]
    )

    event_entry_message_data_dict = json.loads(event_entry_message_data.json())

    assert event_entry_message_data_dict == {
        "mid": "mid",
        "text": "text",
        "attachments": [message_attachment_dict],
    }

    event_entry_message_data = EventEntryMessageData.parse_obj(
        event_entry_message_data_dict
    )

    assert event_entry_message_data == EventEntryMessageData(
        mid="mid", text="text", attachments=[message_attachment]
    )

    event_entry_message = EventEntryMessage(
        sender=event_entry_message_sender,
        recipient=event_entry_message_recipient,
        timestamp=60000,
        message=event_entry_message_data,
        postback=message_postback,
        referral=referral_data,
    )

    event_entry_message_dict = json.loads(event_entry_message.json())

    assert event_entry_message_dict == {
        "sender": event_entry_message_sender_dict,
        "recipient": event_entry_message_recipient_dict,
        "timestamp": 60000,
        "message": event_entry_message_data_dict,
        "postback": message_postback_dict,
        "referral": referral_data_dict,
    }

    event_entry_message = EventEntryMessage.parse_obj(event_entry_message_dict)

    assert event_entry_message == EventEntryMessage(
        sender=event_entry_message_sender,
        recipient=event_entry_message_recipient,
        timestamp=60000,
        message=event_entry_message_data,
        postback=message_postback,
        referral=referral_data,
    )

    event_entry = EventEntry(id="id", time=60000, messaging=[event_entry_message])

    event_entry_dict = json.loads(event_entry.json())

    assert event_entry_dict == {
        "id": "id",
        "time": 60000,
        "messaging": [event_entry_message_dict],
    }

    event_entry = EventEntry.parse_obj(event_entry_dict)

    assert event_entry == EventEntry(
        id="id", time=60000, messaging=[event_entry_message]
    )

    incoming_event = IncomingEvent(object="object", entry=[event_entry])

    incoming_event_dict = json.loads(incoming_event.json())

    assert incoming_event_dict == {"object": "object", "entry": [event_entry_dict]}

    incoming_event = IncomingEvent.parse_obj(incoming_event_dict)

    assert incoming_event == IncomingEvent(object="object", entry=[event_entry])


def test_outgoing_models():

    generic_template_button = GenericTemplateButton(
        type="type", title="title", payload="payload", url="url"
    )

    generic_template_button_dict = json.loads(generic_template_button.json())

    assert generic_template_button_dict == {
        "type": "type",
        "title": "title",
        "payload": "payload",
        "url": "url",
    }

    generic_template_button = GenericTemplateButton.parse_obj(
        generic_template_button_dict
    )

    assert generic_template_button == GenericTemplateButton(
        type="type", title="title", payload="payload", url="url"
    )

    generic_template_element = GenericTemplateElement(
        title="title",
        image_url="image url",
        subtitle="subtitle",
        buttons=[generic_template_button],
    )

    generic_template_element_dict = json.loads(generic_template_element.json())

    assert generic_template_element_dict == {
        "title": "title",
        "image_url": "image url",
        "subtitle": "subtitle",
        "buttons": [generic_template_button_dict],
    }

    generic_template_element = GenericTemplateElement.parse_obj(
        generic_template_element_dict
    )

    assert generic_template_element == GenericTemplateElement(
        title="title",
        image_url="image url",
        subtitle="subtitle",
        buttons=[generic_template_button],
    )

    quick_reply = QuickReply(
        content_type="content type",
        title="title",
        payload="payload",
        image_url="image url",
    )

    quick_reply_dict = json.loads(quick_reply.json())

    assert quick_reply_dict == {
        "content_type": "content type",
        "title": "title",
        "payload": "payload",
        "image_url": "image url",
    }

    quick_reply = QuickReply.parse_obj(quick_reply_dict)

    assert quick_reply == QuickReply(
        content_type="content type",
        title="title",
        payload="payload",
        image_url="image url",
    )

    message_data_attachment_payload = MessageDataAttachmentPayload(
        template_type="template type",
        text="text",
        buttons=[generic_template_button],
        elements=[generic_template_element],
    )

    message_data_attachment_payload_dict = json.loads(
        message_data_attachment_payload.json()
    )

    assert message_data_attachment_payload_dict == {
        "template_type": "template type",
        "text": "text",
        "buttons": [generic_template_button_dict],
        "elements": [generic_template_element_dict],
    }

    message_data_attachment_payload = MessageDataAttachmentPayload.parse_obj(
        message_data_attachment_payload_dict
    )

    assert message_data_attachment_payload == MessageDataAttachmentPayload(
        template_type="template type",
        text="text",
        buttons=[generic_template_button],
        elements=[generic_template_element],
    )

    message_data_attachment = MessageDataAttachment(
        type="type", payload=message_data_attachment_payload
    )

    message_data_attachment_dict = json.loads(message_data_attachment.json())

    assert message_data_attachment_dict == {
        "type": "type",
        "payload": message_data_attachment_payload_dict,
    }

    message_data_attachment = MessageDataAttachment.parse_obj(
        message_data_attachment_dict
    )

    assert message_data_attachment == MessageDataAttachment(
        type="type", payload=message_data_attachment_payload
    )

    message_data = MessageData(
        text="text", attachment=message_data_attachment, quick_replies=[quick_reply]
    )

    message_data_dict = json.loads(message_data.json())

    assert message_data_dict == {
        "text": "text",
        "attachment": message_data_attachment_dict,
        "quick_replies": [quick_reply_dict],
    }

    message_data = MessageData.parse_obj(message_data_dict)

    assert message_data == MessageData(
        text="text", attachment=message_data_attachment, quick_replies=[quick_reply]
    )

    message_recipient = MessageRecipient(id="id", email="e-mail")

    message_recipient_dict = json.loads(message_recipient.json())

    assert message_recipient_dict == {"id": "id", "email": "e-mail"}

    message_recipient = MessageRecipient.parse_obj(message_recipient_dict)

    assert message_recipient == MessageRecipient(id="id", email="e-mail")

    message = Message(
        recipient=message_recipient,
        messaging_type="messaging type",
        message=message_data,
    )

    message_dict = json.loads(message.json())

    assert message_dict == {
        "recipient": message_recipient_dict,
        "messaging_type": "messaging type",
        "message": message_data_dict,
    }

    message = Message.parse_obj(message_dict)

    assert message == Message(
        recipient=message_recipient,
        messaging_type="messaging type",
        message=message_data,
    )
