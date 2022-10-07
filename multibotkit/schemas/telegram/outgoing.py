from typing import Optional, List, Union

from pydantic import Field
from pydantic.main import BaseModel


class SetWebhookParams(BaseModel):
    url: str = Field(..., title="HTTPS url to send updates to")
    ip_address: Optional[str] = Field(
        None,
        title="The fixed IP address which will be used to send webhook \
requests instead of the IP address resolved through DNS",
    )
    max_connections: Optional[int] = Field(
        None,
        title="Maximum allowed number of simultaneous HTTPS connections \
to the webhook for update delivery, 1-100",
    )
    allowed_updates: Optional[List[str]] = Field(
        None,
        title="A JSON-serialized list of the update types you want your \
                bot to receive",
        description="For example, specify [“message”, \
“edited_channel_post”, “callback_query”] to only receive \
updates of these types. See Update for a complete list of \
available update types. Specify an empty list to receive \
all update types except chat_member (default). \
If not specified, the previous setting will be used.\
Please note that this parameter doesn't affect updates \
created before the call to the setWebhook, so unwanted \
updates may be received for a short period of time.",
    )


class WebhookInfo(BaseModel):
    url: str = Field(..., title="Webhook URL, may be empty if webhook is not set up")
    has_custom_certificate: Optional[bool] = Field(
        None,
        title="True, if a custom certificate was provided for webhook \
certificate checks",
    )
    pending_update_count: Optional[int] = Field(
        None, title="Number of updates awaiting delivery"
    )
    ip_address: Optional[str] = Field(None, title="Currently used webhook IP address")
    last_error_date: Optional[int] = Field(
        None,
        title="Unix time for the most recent error that happened when \
trying to deliver an update via webhook",
    )
    last_error_message: Optional[str] = Field(
        None,
        title="Error message in human-readable format for the most \
recent error that happened when trying to deliver \
an update via webhook",
    )
    max_connections: Optional[int] = Field(
        None,
        title="Maximum allowed number of simultaneous HTTPS connections \
to the webhook for update delivery",
    )
    allowed_updates: Optional[List[str]] = Field(
        None, title="A list of update types the bot is subscribed to"
    )


class InlineKeyboardButton(BaseModel):
    text: str = Field(..., title="Label text on the button")
    url: Optional[str] = Field(
        None, title="HTTP or tg:// url to be opened when button is pressed"
    )
    callback_data: Optional[str] = Field(
        None,
        title=" Data to be sent in a callback query to the bot \
when button is pressed, 1-64 bytes",
    )


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboardButton]] = Field(
        ...,
        title="Array of button rows, each represented by an \
Array of InlineKeyboardButton objects",
    )


class KeyboardButton(BaseModel):
    text: str = Field(..., title="Text of the button")
    request_contact: Optional[bool] = Field(
        None,
        title=" If True, the user's phone number will be sent as a \
contact when the button is pressed",
    )
    request_location: Optional[bool] = Field(
        None,
        title="If True, the user's current location will be sent \
when the button is pressed",
    )


class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[List[KeyboardButton]] = Field(
        ...,
        title="Array of button rows, each represented by an \
Array of KeyboardButton objects",
    )
    resize_keyboard: Optional[bool] = Field(
        None,
        title="Requests clients to resize the keyboard vertically \
for optimal fit",
    )
    one_time_keyboard: Optional[bool] = Field(
        None,
        title="Requests clients to hide the keyboard as soon as \
it's been used",
    )


class Message(BaseModel):
    chat_id: int = Field(..., title="Unique identifier for the chat")
    text: str = Field(
        ..., title="For text messages, the actual UTF-8 text of the message"
    )
    disable_web_page_preview: Optional[bool] = Field(
        None, title="Disables link previews for links in this message"
    )
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = Field(
        None, title="Inline or Reply keyboard attached to the message"
    )


class InputMedia(BaseModel):
    type: str
    media: Union[str, tuple] = Field(...)
    caption: Optional[str] = Field(None)
    parse_mode: Optional[str] = Field(None)


class InputMediaPhoto(InputMedia):
    type: str = "photo"
    media: str = Field(...)


class InputMediaDocument(InputMedia):
    type: str = "document"


class MediaGroup(BaseModel):
    chat_id: int = Field(...)
    media: Union[List[InputMediaPhoto], List[InputMediaDocument]] = Field(...)


class Photo(BaseModel):
    chat_id: int = Field(..., title="chat id")
    photo: str = Field(..., title="photo")
    caption: Optional[str] = Field(None, title="caption")
    parse_mode: str = Field("HTML", title="parse mode")
    disable_notification: Optional[bool] = Field(None, title="disable notification")
    protect_content: Optional[bool] = Field(None, title="protect content")
    reply_to_message_id: Optional[int] = Field(None, title="reply to message id")
    allow_sending_without_reply: Optional[bool] = Field(None, title="allow sending without reply")
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = Field(None, title="reply markup")


class EditMessageMediaModel(BaseModel):
    chat_id: Optional[int] = Field(None, title="chat id")
    message_id: Optional[int] = Field(None, title="message id")
    inline_message_id: Optional[str] = Field(None, title="inline message id")
    media: InputMedia = Field(..., title="media")
    reply_markup: Optional[InlineKeyboardMarkup] = Field(None, title="reply markup")
