from typing import Optional, List

from pydantic import BaseModel, Field


class KeyboardAction(BaseModel):
    type: str = Field(
        "text", title="Action type", description="for the text button the value is text"
    )
    label: Optional[str] = Field(
        None,
        title="Button text",
        description="It is sent by the user to the chat after pressing",
    )
    payload: str = Field(
        ...,
        title="Additional information",
        description="It is returned in the messages_new event inside \
the payload property",
    )


class KeyboardButton(BaseModel):
    action: KeyboardAction = Field(
        ...,
        title="An object that describes the type \
of action and its parameters.",
        description="Object fields depend on the type parameter \
and are described in the table below.",
    )
    color: Optional[str] = Field(
        None,
        title="Button color.",
        description="This parameter is used only for buttons \
with the text type. \
Possible values: \n\
    primary – blue button, indicates the main action. #5181B8\n\
    secondary – default white button. #FFFFFF\n\
    negative – dangerous or negative action \
        (cancel, delete etc.) #E64646\n\
    positive – accept, agree. #4BB34B",
    )


class Keyboard(BaseModel):
    one_time: bool = Field(
        False,
        title="Hides the keyboard after the initial use.",
        description="This parameter only works for buttons \
that send a message (type field – text, location). \
For open_app and vk_pay type, this parameter is ignored.",
    )
    inline: bool = Field(False, title="Shows the keyboard inside the message. ")
    buttons: List[List[KeyboardButton]] = Field(..., title="An array of button arrays.")


class Message(BaseModel):
    user_id: int = Field(..., title="User ID (by default — current user).")
    message: Optional[str] = Field(
        None, title="(Required if attachments is not set.) Text of the message."
    )
    keyboard: Optional[Keyboard] = Field(None)
    lat: Optional[float] = Field(
        None,
        title="Geographical latitude of a check-in, in degrees \
(from -90 to 90).",
    )
    long: Optional[float] = Field(
        None,
        title="Geographical longitude of a check-in, in degrees \
(from -90 to 90).",
    )
    attachment: Optional[str] = Field(
        None,
        title="(Required if message is not set.) \
List of objects attached to the message, separated by commas",
    )
    template: Optional[dict] = Field(
        None,
        title="Bots can send special messages using templates.",
        description="Such messages differ from regular ones both visually \
and functionally. Currently, the carousel is the only template \
available.",
    )


class Element(BaseModel):
    title: str = Field(None, title="Title", description="maximum 80 characters")
    description: str = Field(
        None, title="Subtitle", description="maximum 80 characters"
    )
    photo_id: str = Field(
        None,
        title="ID of an image that needs to be attached",
        description="Image ratio: 13/8\n\
Minimum dimensions: 221x136\n\
Image upload for the carousel is the same as image \
upload in messages by bots",
    )
    buttons: List[KeyboardButton] = Field(
        None,
        title="Array with buttons",
        description="Can pass any button that is described here. \
One carousel element can contain up to 3 buttons.",
    )
    action: dict = Field(
        {"type": "open_photo"},
        title="An object describing the action that needs to happen \
after a carousel element is clicked",
        description="The following two actions are supported:\n\
open_link - opens a link from the 'link' field.\n\
open_photo - opens an image from the current carousel \
element.",
    )


class Template(BaseModel):
    type: str = Field("carousel")
    elements: List[Element] = Field(...)
