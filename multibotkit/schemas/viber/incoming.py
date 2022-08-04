from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class Location(BaseModel):
    lat: str = Field(..., title="Latitude", description="±90°")
    lon: str = Field(..., title="Longitude", description="±180°")


class Contact(BaseModel):
    name: str = Field(..., title="Name of the contact", description="Max 28 characters")
    phone_number: str = Field(
        ...,
        title="Phone number of the contact",
        description="Max 18 characters. \
Only one phone_number per contact can be sent",
    )
    avatar: Optional[str] = Field(None, title="The avatar URL")


class Message(BaseModel):
    type: str = Field(
        ...,
        title="Message type",
        description="text / picture / video / file / sticker / \
contact / url / location",
    )
    text: Optional[str] = Field(None, title="The message text")
    media: Optional[str] = Field(
        None,
        title="URL of the message media - can be image, video, file \
and url. Image/Video/File URLs will have a TTL of 1 hour",
    )
    location: Optional[Location] = Field(None, title="Location coordinates")
    contact: Optional[Contact] = Field(None, title="Contact data")
    tracking_data: Optional[str] = Field(
        None, title="Tracking data sent with the last message to the user"
    )
    file_name: Optional[str] = Field(
        None, title="File name", description="Relevant for file type messages"
    )
    file_size: Optional[int] = Field(
        None, title="File size in bytes", description="Relevant for file type messages"
    )
    duration: Optional[int] = Field(
        None,
        title="Video length in seconds",
        description="Relevant for video type messages",
    )
    sticker_id: Optional[int] = Field(
        None, title="Viber sticker id", description="Relevant for sticker type messages"
    )


class User(BaseModel):
    id: str = Field(..., title="Unique Viber user id")
    name: str = Field(..., title="User’s Viber name")
    avatar: str = Field(..., title="URL of user’s avatar")
    country: str = Field(
        ..., title="User’s 2 letter country code", description="ISO ALPHA-2 Code"
    )
    language: str = Field(
        ...,
        title="User’s phone language. Will be returned according \
to the device language",
        description="ISO 639-1",
    )
    api_version: int = Field(
        1,
        title="The maximal Viber version that is supported by all \
of the user’s devices",
        description="Currently only 1. Additional versions will be added \
in the future",
    )


class ReceivingMessageCallback(BaseModel):
    sender: Optional[User] = Field(None, title="Sender data")
    message: Optional[Message] = Field(None, title="Message data")


class SubscriptionCallback(BaseModel):
    user: Optional[User] = Field(None, title="User data")


class UnsubscribeCallback(BaseModel):
    user_id: Optional[str] = Field(None, title="User id data")


class ConversationStartedCallback(BaseModel):
    type: Optional[str] = Field(
        None,
        title="The specific type of conversation_started event",
        description="Additional types may be added in the future",
    )
    context: Optional[str] = Field(
        None,
        title="Any additional parameters added to the deep link \
used to access the conversation passed as a string",
    )
    user: Optional[User] = Field(None, title="User data")
    subscribed: Optional[bool] = Field(
        None,
        title="indicated whether a user is already subscribed",
        description="true if subscribed and false otherwise",
    )


class FailedCallback(BaseModel):
    user_id: Optional[str] = Field(None, title="User id data")
    desc: Optional[str] = Field(None, title="A string describing the failure")


class Callback(
    ReceivingMessageCallback,
    SubscriptionCallback,
    UnsubscribeCallback,
    ConversationStartedCallback,
    FailedCallback,
):
    event: str = Field(..., title="Callback type - which event triggered the callback")
    timestamp: int = Field(..., title="Time of the event that triggered the callback")
    message_token: int = Field(..., title="Unique ID of the message")
