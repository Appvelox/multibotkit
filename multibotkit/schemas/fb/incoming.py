from typing import List, Optional

from pydantic import BaseModel, Field


class EventEntryMessageRecipient(BaseModel):
    id: str = Field(..., title="Your Page ID.")


class EventEntryMessageSender(BaseModel):
    id: str = Field(..., title="The PSID of the user that triggered the webhook event.")


class MessageAttachmentPayload(BaseModel):
    url: str = Field(
        ...,
        title="URL of the attachment type.",
        description="Applicable to attachment type: \
audio, file, image, video, fallback",
    )


class MessageAttachment(BaseModel):
    type: str = Field(..., title="audio, file, image, video or fallback")
    payload: MessageAttachmentPayload = Field(...)


class ReferralData(BaseModel):
    ref: str = Field(
        ...,
        title="The optional ref attribute set in the referrer.",
        description="Only alphanumeric characters as well \
as -, _, and = are supported.",
    )
    source: str = Field(
        ...,
        title="The source of the referral.",
        description="Supported values:\n\
    1. ADS\n\
    2. SHORTLINK\n\
    3. CUSTOMER_CHAT_PLUGIN",
    )
    type: str = Field(
        ..., title="The referral type", description="Currently supports OPEN_THREAD."
    )


class MessagePostback(BaseModel):
    title: str = Field(
        ...,
        title="Title for the CTA that was clicked on.",
        description="This is sent to all apps subscribed to the page. \
For apps other than the original CTA sender, \
the postback event will be delivered via the standby channel.",
    )
    payload: str = Field(
        ...,
        title="payload parameter that was defined with the button.",
        description="This is only visible to the app that send \
the original template message.",
    )
    referral: Optional[ReferralData] = Field(
        None, title="Referral information for how the user got into the thread."
    )


class EventEntryMessageData(BaseModel):
    mid: str = Field(..., title="Message ID")
    text: Optional[str] = Field(None, title="Text of message")
    attachments: List[MessageAttachment] = Field(
        [], title="Array containing attachment data"
    )


class EventEntryMessage(BaseModel):
    sender: EventEntryMessageSender = Field(...)
    recipient: EventEntryMessageRecipient = Field(...)
    timestamp: int = Field(...)
    message: Optional[EventEntryMessageData] = Field(None)
    postback: Optional[MessagePostback] = Field(None)
    referral: Optional[ReferralData] = Field(
        None, title="Referral of the message from Shops product details page."
    )


class EventEntry(BaseModel):
    id: str = Field(..., title="Page ID of page")
    time: int = Field(
        ..., title="Time of update.", description="Epoch time in milliseconds"
    )
    messaging: List[EventEntryMessage] = Field(
        ...,
        title="Array containing one messaging object.",
        description="Note that even though this is an array, \
it will only contain one messaging object.",
    )


class IncomingEvent(BaseModel):
    object: str = Field(..., title="Value will be page")
    entry: List[EventEntry] = Field(..., title="Array containing event data")
