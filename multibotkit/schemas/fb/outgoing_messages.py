from typing import Optional, List

from pydantic import BaseModel, Field


class GenericTemplateButton(BaseModel):
    type: str = Field("postback", title="Type of button.")
    title: str = Field(..., title="Button title.", description="20 character limit.")
    payload: Optional[str] = Field(
        None,
        title="This data will be sent back to your webhook.",
        description="1000 character limit.",
    )
    url: Optional[str] = Field(
        None, title="This URL is opened in a mobile browser when the button is tapped."
    )


class GenericTemplateElement(BaseModel):
    title: str = Field(
        ...,
        title="The title to display in the template.",
        description="80 character limit.",
    )
    image_url: Optional[str] = Field(
        None, title="The URL of the image to display in the template."
    )
    subtitle: Optional[str] = Field(
        None,
        title="The subtitle to display in the template.",
        description="80 character limit.",
    )
    buttons: List[GenericTemplateButton] = Field(
        ...,
        title="An array of buttons to append to the template.",
        description="A maximum of 3 buttons per element is supported.",
    )


class QuickReply(BaseModel):
    content_type: str = Field(
        "text",
        title="Must be one of the following:",
        description="1. text: Sends a text button\n\
            2. user_phone_number: Sends a button allowing recipient \
                to send the phone number associated with their account\n\
            3. user_email: Sends a button allowing recipient \
                to send the email associated with their account.",
    )
    title: str = Field(
        ...,
        title="The text to display on the quick reply button.",
        description="Required if content_type is 'text'. 20 character limit.",
    )
    payload: str = Field(
        ...,
        title="Custom data that will be sent back to you \
            via the messaging_postbacks webhook event.",
        description="Required if content_type is 'text'. 1000 character limit.",
    )
    image_url: Optional[str] = Field(
        None,
        title="URL of image to display on the quick reply button for text quick replies.",
        description="Image should be a minimum of 24px x 24px. \
            Larger images will be automatically cropped and resized. \
            Required if title is an empty string.",
    )


class MessageDataAttachmentPayload(BaseModel):
    template_type: str = Field("generic")
    text: Optional[str] = Field(
        None,
        title="UTF-8-encoded text of up to 640 characters.",
        description="Text will appear above the buttons.",
    )
    buttons: Optional[List[GenericTemplateButton]] = Field(
        None, title="Set of 1-3 buttons that appear as call-to-actions."
    )
    elements: Optional[List[GenericTemplateElement]] = Field(
        None,
        title="An array containing 1 element object that describe the media in the message.",
        description="A maximum of 1 element is supported.",
    )


class MessageDataAttachment(BaseModel):
    type: str = Field(
        ...,
        title="Type of attachment",
        description="May be image, audio, video, file or template. \
            For assets, max file size is 25MB.",
    )
    payload: MessageDataAttachmentPayload = Field(
        ...,
        title="Payload of attachment",
        description="Can either be a Template Payload or a File Attachment Payload",
    )


class MessageData(BaseModel):
    text: Optional[str] = Field(
        None,
        title="Message text",
        description="Previews will not be shown for the URLs in this field. \
            Use attachment instead. Must be UTF-8 and has a 2000 character limit. \
            text or attachment must be set.",
    )
    attachment: Optional[MessageDataAttachment] = Field(
        None,
        title="Attachment object",
        description="Previews the URL. \
            Used to send messages with media or Structured Messages. \
            text or attachment must be set.",
    )
    quick_replies: Optional[List[QuickReply]] = Field(
        None, title="Array of quick_reply to be sent with messages"
    )


class MessageRecipient(BaseModel):
    id: Optional[str] = Field(
        None,
        title="Page Scoped User ID (PSID) of the message recipient.",
        description="The user needs to have interacted with any \
            of the Messenger entry points in order to opt-in into messaging \
            with the Page. \
            Note that Facebook Login integrations return user IDs \
            are app-scoped and will not work with the Messenger platform.",
    )
    email: Optional[str] = Field(None, title="Recipient e-mail")


class Message(BaseModel):
    recipient: MessageRecipient = Field(..., title="recipient object")
    messaging_type: str = Field(
        "RESPONSE",
        title="The messaging type of the message being sent.",
        description="For supported types and more information, \
            see Sending Messages - Messaging Types",
    )
    message: MessageData = Field(..., title="Message object")
