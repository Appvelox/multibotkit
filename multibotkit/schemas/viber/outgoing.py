from enum import Enum
from typing import Optional, List

from pydantic import Field
from pydantic.main import BaseModel


class Button(BaseModel):
    Columns: Optional[int] = Field(6, ge=1, le=6, title="Button width in columns")
    Rows: Optional[int] = Field(1, ge=1, le=2, title="Button height in rows")
    Text: Optional[str] = Field(
        None,
        title="Text to be displayed on the button",
        description="Free text. Valid and allowed HTML tags \
Max 250 characters. If the text is too long to display \
on the button it will be cropped and ended with “…”",
    )
    TextSize: str = Field(
        "regular", title="Text size out of 3 available options: small, regular, large"
    )
    TextHAlign: str = Field(
        "center", title="Horizontal align of the text: left, center, right"
    )
    TextVAlign: str = Field(
        "center", title="Vertical alignment of the text: top, middle, bottom"
    )
    ActionType: str = Field(
        "reply",
        title="Type of action pressing the button will perform. \
Reply - will send a reply to the bot. open-url - will \
open the specified URL and send the URL as reply to the bot. \
location-picker and share-phone are not \
supported on desktop, and require adding any text in the \
ActionBody parameter",
        description="reply / open-url / location-picker / \
share-phone / none",
    )
    ActionBody: str = Field(
        ...,
        title="Text for reply and none. ActionType or URL for open-url",
        description="For ActionType reply - text \
For ActionType open-url - Valid URL.",
    )
    BgColor: Optional[str] = Field(
        None, title="Background color of button", description="Valid color HEX value"
    )
    Image: Optional[str] = Field(
        None,
        title="URL of image to place on top of background",
        description="Can be a partially transparent image \
that will allow showing some of the background. \
Will be placed with aspect to fill logic. \
Valid URL. JPEG and PNG files are supported. \
Max size: 500 kb",
    )


class Keyboard(BaseModel):
    Type: str = Field("keyboard")
    DefaultHeight: bool = Field(
        False,
        title="When true - the keyboard will always be displayed \
with the same height as the native keyboard.When \
false - short keyboards will be displayed with \
the minimal possible height",
    )
    BgColor: Optional[str] = Field(None, title="Background color of the keyboard")
    Buttons: List[Button] = Field(
        ..., title="Array containing all keyboard buttons by order"
    )


class SetWebhook(BaseModel):
    url: str = Field(
        ..., title="Account webhook URL to receive callbacks & messages from users"
    )
    event_types: Optional[List[str]] = Field(
        None,
        title="Indicates the types of Viber events that \
the account owner would like to be notified about",
    )
    send_name: bool = Field(
        False, title=" Indicates whether or not the bot should receive the user name"
    )
    send_photo: bool = Field(
        False, title=" Indicates whether or not the bot should receive the user photo"
    )


class Sender(BaseModel):
    name: str = Field(
        ..., title="The sender’s name to display", description="Max 28 characters"
    )
    avatar: Optional[str] = Field(
        None,
        title="The sender’s avatar URL",
        description="Avatar size should be no more than 100 kb. \
Recommended 720x720",
    )


class Contact(BaseModel):
    name: str = Field(..., title="Name of the contact", description="Max 28 characters")
    phone_number: str = Field(
        ..., title="Phone number of the contact", description="Max 18 characters"
    )


class Location(BaseModel):
    lat: str = Field(..., title="Latitude", description="±90°")
    lon: str = Field(..., title="Longitude", description="±180°")


class MessageType(str, Enum):
    text = ("text",)
    picture = ("picture",)
    video = ("video",)
    file = ("file",)
    contact = ("contact",)
    location = ("location",)
    url = ("url",)
    sticker = "sticker"


class BaseMessage(BaseModel):
    receiver: str = Field(
        ...,
        title="Unique Viber user id",
        description="required, subscribed valid user id",
    )
    min_api_version: int = Field(
        7,
        title="Minimal API version required by clients \
for this message (default 1)",
        description="optional. client version support the API version. \
Certain features may not work as expected \
if set to a number that’s below their requirements.",
    )
    sender: Sender = Field(None, title="Sender object")
    tracking_data: Optional[str] = Field(
        None,
        title="Allow the account to track messages and user’s replies. \
Sent tracking_data value will be passed back with user’s reply",
        description="max 4000 characters",
    )
    keyboard: Keyboard = Field(None)


class TextMessage(BaseMessage):
    type: MessageType = Field(
        "text", title="Message type", description="text. Supports text formatting"
    )
    text: str = Field(
        ..., title="The text of the message", description="Max length 7,000 characters"
    )


class PictureMessage(BaseMessage):
    type: MessageType = Field("picture", title="Message type", description="picture")
    text: str = Field(
        ...,
        title="Description of the photo. \
Can be an empty string if irrelevant",
        description="Max 512 characters",
    )
    media: str = Field(
        ...,
        title="URL of the image (JPEG, PNG, non-animated GIF)",
        description="The URL must have a resource \
with a .jpeg, .png or .gif file extension as the \
last path segment. \
Example: http://www.example.com/path/image.jpeg. \
Animated GIFs can be sent as URL messages or file messages. \
Max image size: 1MB on iOS, 3MB on Android.",
    )
    thumbnail: Optional[str] = Field(
        None,
        title="URL of a reduced size image (JPEG, PNG, GIF)",
        description="Recommended: 400x400. Max size: 100kb.",
    )


class VideoMessage(BaseMessage):
    type: MessageType = Field("video", title="Message type")
    media: str = Field(
        ...,
        title="URL of the video (MP4, H264)",
        description="Max size 26 MB. Only MP4 and H264 are supported. \
The URL must have a resource with a .mp4 file extension \
as the last path segment. \
Example: http://www.example.com/path/video.mp4",
    )
    thumbnail: Optional[str] = Field(
        None,
        title="URL of a reduced size video (JPEG, PNG, GIF)",
        description="Max size 100 kb. Recommended: 400x400. \
Only JPEG format is supported",
    )
    size: int = Field(..., title="Size of the video in bytes")
    duration: Optional[int] = Field(
        None,
        title="Video duration in seconds; will be displayed \
to the receiver",
        description="Max 180 seconds",
    )


class FileMessage(BaseMessage):
    type: MessageType = Field("file", title="Message type")
    media: str = Field(
        ...,
        title="URL of the file",
        description="Max size 50 MB. \
See forbidden file formats for unsupported file types",
    )
    size: int = Field(..., title="Size of the file in bytes")
    file_name: str = Field(
        ...,
        title="Name of the file",
        description=" File name should include extension. \
Max 256 characters (including file extension). \
Sending a file without extension or with the wrong extension \
might cause the client to be unable to open the file",
    )


class ContactMessage(BaseMessage):
    type: MessageType = Field("contact", title="Message type")
    contact: Contact = Field(..., title="Contact info")


class LocationMessage(BaseMessage):
    type: MessageType = Field("location", title="Message type")
    location: Location = Field(..., title="Location coordinates")


class UrlMessage(BaseMessage):
    type: MessageType = Field("url", title="Message type")
    media: str = Field(..., title="URL", description="Max 2,000 characters")


class StickerMessage(BaseMessage):
    type: MessageType = Field("sticker", title="Message type")
    sticker_id: int = Field(
        ...,
        title="Unique Viber sticker ID",
        description="For examples visit the sticker IDs page",
    )
