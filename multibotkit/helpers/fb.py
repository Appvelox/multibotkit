from typing import List, Optional
from multibotkit.helpers.base_helper import BaseHelper
from multibotkit.schemas.fb.outgoing import (
    Message,
    MessageData,
    MessageDataAttachment,
    MessageRecipient,
    PersistentMenu,
    QuickReply,
)


class FBHelper(BaseHelper):
    class _SendMessageArgumentsError(Exception):
        pass

    def __init__(
        self,
        token: str,
        messages_endpoint: str = "https://graph.facebook.com/v14.0/me/messages?access_token=",
        profile_endpoint: str = "https://graph.facebook.com/v14.0/me/messenger_profile?access_token=",
    ):
        self.MESSAGES_URL = messages_endpoint + token
        self.PROFILE_URL = profile_endpoint + token

    def __build_message(
        self,
        recipient_id: str,
        message_type: str = "RESPONSE",
        text: Optional[str] = None,
        attachment: Optional[MessageDataAttachment] = None,
        quick_replies: Optional[List[QuickReply]] = None,
    ):
        recipient = MessageRecipient(id=recipient_id)
        data = MessageData(
            text=text, attachment=attachment, quick_replies=quick_replies
        )
        message = Message(
            recipient=recipient, messaging_type=message_type, message=data
        )
        return message

    def sync_send_message(
        self,
        recipient_id: str,
        message_type: str = "RESPONSE",
        text: Optional[str] = None,
        attachment: Optional[MessageDataAttachment] = None,
        quick_replies: Optional[List[QuickReply]] = None,
    ):
        if (text is None) and (attachment is None) and (quick_replies is None):
            raise self._SendMessageArgumentsError(
                "Message has to contain a text or an attachment or \
a list of quick replies"
            )

        message = self.__build_message(
            recipient_id=recipient_id,
            message_type=message_type,
            text=text,
            attachment=attachment,
            quick_replies=quick_replies,
        )

        data = message.json(exclude_none=True)
        r = self._perform_sync_request(url=self.MESSAGES_URL, data=data)
        return r

    async def async_send_message(
        self,
        recipient_id: str,
        message_type: str = "RESPONSE",
        text: Optional[str] = None,
        attachment: Optional[MessageDataAttachment] = None,
        quick_replies: Optional[List[QuickReply]] = None,
    ):
        if (text is None) and (attachment is None) and (quick_replies is None):
            raise self._SendMessageArgumentsError(
                "Message has to contain a text or an attachment or \
a list of quick replies"
            )

        message = self.__build_message(
            recipient_id=recipient_id,
            message_type=message_type,
            text=text,
            attachment=attachment,
            quick_replies=quick_replies,
        )

        data = message.json(exclude_none=True)
        r = await self._perform_async_request(url=self.MESSAGES_URL, data=data)
        return r

    def sync_send_get_started(self, payload: str = "GET_STARTED"):
        data = {"get_started": {"payload": payload}}
        r = self._perform_sync_request(url=self.PROFILE_URL, data=data)
        return r

    async def async_send_get_started(self, payload: str = "GET_STARTED"):
        data = {"get_started": {"payload": payload}}
        r = await self._perform_async_request(url=self.PROFILE_URL, data=data)
        return r

    def sync_send_greeting(self, text: str):
        data = {"greeting": [{"locale": "default", "text": text}]}
        r = self._perform_sync_request(self.PROFILE_URL, data=data)
        return r

    async def async_send_greeting(self, text: str):
        data = {"greeting": [{"locale": "default", "text": text}]}
        r = await self._perform_async_request(self.PROFILE_URL, data=data)
        return r

    def sync_send_persistent_menu(self, persistent_menu: PersistentMenu):
        data = persistent_menu.dict(exclude_none=True)
        r = self._perform_sync_request(self.PROFILE_URL, data=data)
        return r

    async def async_send_persistent_menu(self, persistent_menu: PersistentMenu):
        data = persistent_menu.dict(exclude_none=True)
        r = await self._perform_async_request(self.PROFILE_URL, data=data)
        return r
