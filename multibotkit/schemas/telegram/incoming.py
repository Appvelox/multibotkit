from enum import Enum
from typing import Optional, List

from pydantic import Field
from pydantic.main import BaseModel


class MaskPositionPoint(str, Enum):
    forehead = "forehead"
    eyes = "eyes"
    mouth = "mouth"
    chin = "chin"


class ChatType(str, Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"


class FileBasedObject(BaseModel):
    file_id: str = Field(
        ...,
        title="Identifier for this file, which can be used to download \
or reuse the file",
    )
    file_unique_id: str = Field(
        ...,
        title="Unique identifier for this file, which is supposed to be \
the same over time and for different bots",
    )
    file_size: Optional[int] = Field(None, title="File size, if known")


class Location(BaseModel):
    longitude: float = Field(..., title="Longitude as defined by sender")
    latitude: float = Field(..., title="Latitude as defined by sender")
    horizontal_accuracy: Optional[float] = Field(
        None,
        title="The radius of uncertainty for the location, \
measured in meters; 0-1500",
    )
    live_period: Optional[int] = Field(
        None,
        title="Time relative to the message sending date, \
during which the location can be updated, in seconds",
    )
    heading: Optional[int] = Field(
        None, title="The direction in which user is moving, in degrees; 1-360"
    )
    proximity_alert_radius: Optional[int] = Field(
        None,
        title="Maximum distance for proximity alerts about approaching \
another chat member, in meters",
    )


class Contact(BaseModel):
    phone_number: str = Field(..., title="Contact's phone number")
    first_name: str = Field(..., title="Contact's first name")
    last_name: Optional[str] = Field(None, title="Contact's last name")
    user_id: Optional[int] = Field(None, title="Contact's user identifier in Telegram")
    vcard: Optional[str] = Field(
        None, title="Additional data about the contact in the form of a vCard"
    )


class Voice(FileBasedObject):
    duration: int = Field(
        ..., title="Duration of the audio in seconds as defined by sender"
    )
    mime_type: Optional[str] = Field(
        None, title="MIME type of the file as defined by sender"
    )


class Photo(FileBasedObject):
    width: int = Field(..., title="Photo width")
    height: int = Field(..., title="Photo height")


class MaskPosition(BaseModel):
    point: MaskPositionPoint = Field(
        ...,
        title="The part of the face relative to which the mask should be \
placed. One of “forehead”, “eyes”, “mouth”, or “chin”",
    )
    x_shift: float = Field(
        ...,
        title="Shift by X-axis measured in widths of the mask scaled \
to the face size, from left to right",
    )
    y_shift: float = Field(
        ...,
        title="Shift by Y-axis measured in heights of the mask scaled \
to the face size, from top to bottom",
    )
    scale: float = Field(..., title="Mask scaling coefficient")


class Sticker(FileBasedObject):
    width: int = Field(..., title="Sticker width")
    height: int = Field(..., title="Sticker height")
    is_animated: bool = Field(..., title="True, if the sticker is animated")
    thumb: Optional[Photo] = Field(
        None, title="Sticker thumbnail in the .WEBP or .JPG format"
    )
    emoji: Optional[str] = Field(None, title="Emoji associated with the sticker")
    set_name: Optional[str] = Field(
        None, title="Name of the sticker set to which the sticker belongs"
    )
    mask_position: Optional[MaskPosition] = Field(
        None,
        title="For mask stickers, the position where the mask \
should be placed",
    )


class VideoNote(FileBasedObject):
    length: int = Field(
        ...,
        title="Video width and height (diameter of the video message) \
as defined by sender",
    )
    duration: int = Field(
        ..., title="Duration of the video in seconds as defined by sender"
    )
    thumb: Optional[Photo] = Field(None, title="Video thumbnail")


class Video(FileBasedObject):
    width: int = Field(..., title="Video width as defined by sender")
    height: int = Field(..., title="Video height as defined by sender")
    duration: int = Field(
        ..., title="Duration of the video in seconds as defined by sender"
    )
    thumb: Optional[Photo] = Field(None, title="Video thumbnail")
    file_name: Optional[str] = Field(
        None, title="Original filename as defined by sender"
    )
    mime_type: Optional[str] = Field(
        None, title="Mime type of a file as defined by sender"
    )


class Document(FileBasedObject):
    thumb: Optional[Photo] = Field(
        None, title="Document thumbnail as defined by sender"
    )
    file_name: Optional[str] = Field(
        None, title="Original filename as defined by sender"
    )
    mime_type: Optional[str] = Field(
        None, title="MIME type of the file as defined by sender"
    )


class Audio(FileBasedObject):
    duration: int = Field(
        ..., title="Duration of the audio in seconds as defined by sender"
    )
    performer: Optional[str] = Field(
        None,
        title="Performer of the audio as defined by sender or by \
audio tags",
    )
    title: Optional[str] = Field(
        None, title="Title of the audio as defined by sender or by audio tags"
    )
    file_name: Optional[str] = Field(
        None, title="Original filename as defined by sender"
    )
    mime_type: Optional[str] = Field(
        None, title="MIME type of the file as defined by sender"
    )
    thumb: Optional[Photo] = Field(
        None,
        title="Thumbnail of the album cover to which the music file \
belongs",
    )


class Chat(BaseModel):
    id: int = Field(..., title="Unique identifier for this chat. ")
    type: ChatType = Field(
        ...,
        title="Type of chat, can be either “private”, “group”, \
“supergroup” or “channel”",
    )
    title: Optional[str] = Field(
        None, title="Title, for supergroups, channels and group chats"
    )
    first_name: Optional[str] = Field(
        None, title="First name of the other party in a private chat"
    )
    last_name: Optional[str] = Field(
        None, title="Last name of the other party in a private chat"
    )
    username: Optional[str] = Field(
        None,
        title="Username, for private chats, supergroups and channels \
if available",
    )


class User(BaseModel):
    id: int = Field(..., title="Unique identifier for this user or bot")
    is_bot: bool = Field(..., title="True, if this user is a bot")
    first_name: str = Field(..., title="User's or bot's first name")
    last_name: Optional[str] = Field(None, title="User's or bot's last name")
    username: Optional[str] = Field(None, title="User's or bot's username")
    language_code: Optional[str] = Field(
        None, title="IETF language tag of the user's language"
    )
    can_join_groups: Optional[bool] = Field(
        None, title="True, if the bot can be invited to groups"
    )
    can_read_all_group_messages: Optional[bool] = Field(
        None, title="True, if privacy mode is disabled for the bot"
    )
    supports_inline_queries: Optional[bool] = Field(
        None, title="True, if the bot supports inline queries"
    )


class Message(BaseModel):
    message_id: int = Field(..., title="Unique message identifier inside this chat")
    date: int = Field(..., title="Date the message was sent in Unix time")
    from_: Optional[User] = Field(
        None, title="Sender, empty for messages sent to channels"
    )
    chat: Optional[Chat] = Field(None, title="Conversation the message belongs to")
    text: Optional[str] = Field(None, title="The actual UTF-8 text of the message")
    caption: Optional[str] = Field(
        None,
        title="Caption for the animation, audio, document, photo, \
video or voice",
    )
    audio: Optional[Audio] = Field(
        None, title="Message is an audio file, information about the file"
    )
    document: Optional[Document] = Field(
        None, title="Message is a general file, information about the file"
    )
    photo: Optional[List[Photo]] = Field(
        None, title="Message is a photo, available sizes of the photo"
    )
    sticker: Optional[Sticker] = Field(
        None, title="Message is a sticker, information about the sticker"
    )
    video: Optional[Video] = Field(
        None, title="Message is a video, information about the video"
    )
    video_note: Optional[VideoNote] = Field(
        None,
        title="Message is a video note, information about the \
video message",
    )
    voice: Optional[Voice] = Field(
        None, title="Message is a voice message, information about the file"
    )
    contact: Optional[Contact] = Field(
        None, title="Message is a shared contact, information about the contact"
    )
    location: Optional[Location] = Field(
        None,
        title="Message is a shared location, information about \
the location",
    )

    class Config:
        fields = {"from_": "from"}


class CallbackQuery(BaseModel):
    id: str = Field(..., title="Unique identifier for this query")
    from_: Optional[User] = Field(None, title="Sender data")
    message: Optional[Message] = Field(
        None, title="Message with the callback button that originated the query"
    )
    inline_message_id: Optional[int] = Field(
        None,
        title="Identifier of the message sent via the bot in inline mode, \
that originated the query",
    )
    chat_instance: Optional[str] = Field(
        None,
        title="Global identifier, uniquely corresponding to the chat to \
which the message with the callback button was sent",
    )
    data: Optional[str] = Field(None, title="Data associated with the callback button")
    game_short_name: Optional[str] = Field(
        None,
        title="Short name of a Game to be returned, serves as the \
unique identifier for the game",
    )

    class Config:
        fields = {"from_": "from"}


class Update(BaseModel):
    update_id: int = Field(..., title="Id of incoming bot update")
    message: Optional[Message] = Field(None, title="Message data")
    edited_message: Optional[Message] = Field(None, title="Edited message data")
    callback_query: Optional[CallbackQuery] = Field(None, title="Callback query data")
