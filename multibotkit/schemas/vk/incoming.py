from typing import Optional, List

from pydantic import BaseModel, Field


class ClientInfo(BaseModel):
    button_actions: List[str] = Field(...)
    carousel: bool = Field(...)
    inline_keyboard: bool = Field(...)
    keyboard: bool = Field(...)
    lang_id: int = Field(...)


class CoordinatesObject(BaseModel):
    latitude: float = Field(..., title="Geographical latitude")
    longitude: float = Field(..., title="Geographical longitude")


class GeoObject(BaseModel):
    type: str = Field(..., title="Location type")
    coordinates: CoordinatesObject = Field(..., title="Location coordinates")


class MessageObject(BaseModel):
    attachments: List[dict] = Field(..., title="Array of media-attachments")
    conversation_message_id: int = Field(...)
    date: int = Field(..., title="Date (in Unixtime) when the message was sent")
    from_id: str = Field(..., title="User ID")
    peer_id: str = Field(..., title="Destination ID")
    random_id: int = Field(
        ...,
        title="Parameter used while sending the message \
to avoid double sending",
    )
    fwd_messages: List[dict] = Field(..., title="Array of forwarded messages (if any)")
    ref: Optional[str] = Field(None)
    id: int = Field(..., title="Message ID")
    out: int = Field(
        ...,
        title="Message type. 0 — received, 1 — sent. \
(Not returned for forwarded messages.)",
    )
    important: bool = Field(
        ..., title="True, whether the message is marked as important"
    )
    is_hidden: bool = Field(...)
    text: str = Field(..., title="Message text")
    payload: Optional[str] = Field(None, title="Service field (payload)")
    geo: Optional[GeoObject] = Field(None, title="Information about location")


class EventObject(BaseModel):
    client_info: ClientInfo = Field(...)
    message: MessageObject = Field(..., title="Message oject")


class IncomingEvent(BaseModel):
    type: str = Field(..., title="Event type")
    group_id: int = Field(..., title="Group ID")
    object: Optional[EventObject] = Field(None, title="Event object")
