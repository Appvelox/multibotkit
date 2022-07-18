from typing import Optional, List

from pydantic import BaseModel, Field


class KeyboardAction(BaseModel):
    type: str = Field(...)
    label: Optional[str] = Field(None)
    payload: str = Field(...)


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
    inline: bool = Field(
        False,
        title="Shows the keyboard inside the message. "
    )
    buttons: List[List[KeyboardButton]] = Field(
        ...,
        title="An array of button arrays."
    )


class Message(BaseModel):
    user_id: int = Field(
        ...,
        title="User ID (by default — current user)."
    )
    message: str = Field(
        ...,
        title="(Required if attachments is not set.) Text of the message."
    )
    keyboard: Optional[Keyboard] = Field(None)
    lat: Optional[float] = Field(
        None,
        title="Geographical latitude of a check-in, in degrees \
            (from -90 to 90)."
    )
    long: Optional[float] = Field(
        None,
        title="Geographical longitude of a check-in, in degrees \
            (from -90 to 90)."
    )
    attachment: Optional[str] = Field(
        None,
        title="(Required if message is not set.) \
            List of objects attached to the message, separated by commas",
    )
    template: Optional[dict] = Field(None)


class Element(BaseModel):
    title: str = Field(None)
    description: str = Field(None)
    photo_id: str = Field(None)
    buttons: List[KeyboardButton] = Field(None)
    action: dict = Field({"type": "open_photo"})


class Template(BaseModel):
    type: str = Field("carousel")
    elements: List[Element] = Field(...)
