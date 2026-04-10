from typing import IO, List, Optional, Union

from multibotkit.helpers.base_helper import BaseHelper
from multibotkit.schemas.yandexmessenger.incoming import Update
from multibotkit.schemas.yandexmessenger.outgoing import (
    GetUpdatesParams,
    InlineKeyboard,
    SendFileParams,
    SendImageParams,
    SendTextParams,
    SetWebhookParams,
)


class YandexMessengerHelper(BaseHelper):
    """
    Sync и async функции для Yandex Messenger Bot API.

    Базовый URL: https://botapi.messenger.yandex.net/bot/v1/
    Авторизация: Authorization: OAuth <token>
    """

    def __init__(self, token: str, proxy: Optional[str] = None):
        super().__init__(proxy=proxy)
        self.token = token
        self.base_url = "https://botapi.messenger.yandex.net/bot/v1/"
        self.headers = {"Authorization": f"OAuth {self.token}"}

    def _get_request_headers(self):
        return self.headers

    def sync_send_text(
        self,
        text: str,
        chat_id: Optional[str] = None,
        login: Optional[str] = None,
        payload_id: Optional[str] = None,
        reply_message_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        important: Optional[bool] = None,
        disable_web_page_preview: Optional[bool] = None,
        thread_id: Optional[int] = None,
        inline_keyboard: Optional[InlineKeyboard] = None,
    ) -> dict:
        """
        Синхронная отправка текстового сообщения.

        Args:
            text: Текст сообщения (до 6000 символов)
            chat_id: ID чата (для group/channel)
            login: Login пользователя (для private)
            payload_id: Уникальный ID для дедупликации
            reply_message_id: ID сообщения для ответа
            disable_notification: Отключить уведомление
            important: Отметить как важное
            disable_web_page_preview: Отключить превью ссылок
            thread_id: ID треда
            inline_keyboard: Inline клавиатура

        Returns:
            dict с полями {"ok": true, "message_id": integer}
        """
        url = self.base_url + "messages/sendText/"
        params = SendTextParams(
            text=text,
            chat_id=chat_id,
            login=login,
            payload_id=payload_id,
            reply_message_id=reply_message_id,
            disable_notification=disable_notification,
            important=important,
            disable_web_page_preview=disable_web_page_preview,
            thread_id=thread_id,
            inline_keyboard=inline_keyboard,
        )
        data = params.model_dump(exclude_none=True)

        # Сериализация inline_keyboard если есть
        if inline_keyboard:
            data["inline_keyboard"] = inline_keyboard.model_dump(exclude_none=True)[
                "buttons"
            ]

        return self._perform_sync_request(url, data)

    async def async_send_text(
        self,
        text: str,
        chat_id: Optional[str] = None,
        login: Optional[str] = None,
        payload_id: Optional[str] = None,
        reply_message_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        important: Optional[bool] = None,
        disable_web_page_preview: Optional[bool] = None,
        thread_id: Optional[int] = None,
        inline_keyboard: Optional[InlineKeyboard] = None,
    ) -> dict:
        """Асинхронная версия sync_send_text"""
        url = self.base_url + "messages/sendText/"
        params = SendTextParams(
            text=text,
            chat_id=chat_id,
            login=login,
            payload_id=payload_id,
            reply_message_id=reply_message_id,
            disable_notification=disable_notification,
            important=important,
            disable_web_page_preview=disable_web_page_preview,
            thread_id=thread_id,
            inline_keyboard=inline_keyboard,
        )
        data = params.model_dump(exclude_none=True)

        if inline_keyboard:
            data["inline_keyboard"] = inline_keyboard.model_dump(exclude_none=True)[
                "buttons"
            ]

        return await self._perform_async_request(url, data)

    def sync_send_image(
        self,
        image: Union[str, IO],
        chat_id: Optional[str] = None,
        login: Optional[str] = None,
        thread_id: Optional[int] = None,
    ) -> dict:
        """
        Синхронная отправка изображения.

        Args:
            image: Путь к файлу, file_id или IO объект
            chat_id: ID чата (для group/channel)
            login: Login пользователя (для private)
            thread_id: ID треда

        Returns:
            dict с полями {"ok": true, "message_id": integer}
        """
        url = self.base_url + "messages/sendImage/"
        params = SendImageParams(
            chat_id=chat_id,
            login=login,
            thread_id=thread_id,
        )
        data = params.model_dump(exclude_none=True)

        # Обработка различных типов image
        if isinstance(image, str):
            # Если это путь к файлу с расширением
            if image.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp")):
                with open(image, "rb") as f:
                    files = {"image": f}
                    return self._perform_sync_request(
                        url, data, use_json=False, files=files
                    )
            else:
                # Если это file_id - отправляем как JSON
                data["image"] = image
                return self._perform_sync_request(url, data)
        else:
            # Если это IO объект
            files = {"image": image}
            return self._perform_sync_request(url, data, use_json=False, files=files)

    async def async_send_image(
        self,
        image: Union[str, IO],
        chat_id: Optional[str] = None,
        login: Optional[str] = None,
        thread_id: Optional[int] = None,
    ) -> dict:
        """Асинхронная версия sync_send_image"""
        url = self.base_url + "messages/sendImage/"
        params = SendImageParams(
            chat_id=chat_id,
            login=login,
            thread_id=thread_id,
        )
        data = params.model_dump(exclude_none=True)

        if isinstance(image, str):
            if image.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp")):
                with open(image, "rb") as f:
                    content = f.read()
                files = {"image": content}
                return await self._perform_async_request(
                    url, data, use_json=False, files=files
                )
            else:
                data["image"] = image
                return await self._perform_async_request(url, data)
        else:
            files = {"image": image}
            return await self._perform_async_request(
                url, data, use_json=False, files=files
            )

    def sync_send_file(
        self,
        document: Union[str, IO],
        filename: Optional[str] = None,
        chat_id: Optional[str] = None,
        login: Optional[str] = None,
        thread_id: Optional[int] = None,
    ) -> dict:
        """
        Синхронная отправка файла.

        Args:
            document: Путь к файлу, file_id или IO объект
            filename: Имя файла (для IO объектов)
            chat_id: ID чата (для group/channel)
            login: Login пользователя (для private)
            thread_id: ID треда

        Returns:
            dict с полями {"ok": true, "message_id": integer}
        """
        url = self.base_url + "messages/sendFile/"
        params = SendFileParams(
            chat_id=chat_id,
            login=login,
            thread_id=thread_id,
        )
        data = params.model_dump(exclude_none=True)

        if isinstance(document, str):
            # Если это путь к файлу
            if not document.startswith(("http://", "https://")):
                # Локальный файл
                fname = filename or document.split("/")[-1]
                with open(document, "rb") as f:
                    files = {"document": (fname, f)}
                    return self._perform_sync_request(
                        url, data, use_json=False, files=files
                    )
            else:
                # file_id или URL
                data["document"] = document
                return self._perform_sync_request(url, data)
        else:
            # IO объект
            fname = filename or "file"
            files = {"document": (fname, document)}
            return self._perform_sync_request(url, data, use_json=False, files=files)

    async def async_send_file(
        self,
        document: Union[str, IO],
        filename: Optional[str] = None,
        chat_id: Optional[str] = None,
        login: Optional[str] = None,
        thread_id: Optional[int] = None,
    ) -> dict:
        """Асинхронная версия sync_send_file"""
        url = self.base_url + "messages/sendFile/"
        params = SendFileParams(
            chat_id=chat_id,
            login=login,
            thread_id=thread_id,
        )
        data = params.model_dump(exclude_none=True)

        if isinstance(document, str):
            if not document.startswith(("http://", "https://")):
                fname = filename or document.split("/")[-1]
                with open(document, "rb") as f:
                    content = f.read()
                files = {"document": (fname, content)}
                return await self._perform_async_request(
                    url, data, use_json=False, files=files
                )
            else:
                data["document"] = document
                return await self._perform_async_request(url, data)
        else:
            fname = filename or "file"
            files = {"document": (fname, document)}
            return await self._perform_async_request(
                url, data, use_json=False, files=files
            )

    def sync_get_updates(
        self,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> dict:
        """
        Синхронное получение обновлений (long polling).

        Args:
            limit: Количество обновлений (1-1000, по умолчанию 100)
            offset: Смещение для пагинации

        Returns:
            dict с полями {"ok": true, "updates": [...]}
        """
        url = self.base_url + "messages/getUpdates/"
        params = GetUpdatesParams(limit=limit, offset=offset)
        data = params.model_dump(exclude_none=True)

        return self._perform_sync_request(url, data)

    async def async_get_updates(
        self,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> dict:
        """Асинхронная версия sync_get_updates"""
        url = self.base_url + "messages/getUpdates/"
        params = GetUpdatesParams(limit=limit, offset=offset)
        data = params.model_dump(exclude_none=True)

        return await self._perform_async_request(url, data)

    def sync_set_webhook(
        self,
        webhook_url: Optional[str] = None,
    ) -> dict:
        """
        Синхронная установка webhook.

        Args:
            webhook_url: URL для webhook (None для отключения)

        Returns:
            dict с результатом операции
        """
        url = self.base_url + "self/update/"
        params = SetWebhookParams(webhook_url=webhook_url)
        data = params.model_dump(exclude_none=True)

        return self._perform_sync_request(url, data)

    async def async_set_webhook(
        self,
        webhook_url: Optional[str] = None,
    ) -> dict:
        """Асинхронная версия sync_set_webhook"""
        url = self.base_url + "self/update/"
        params = SetWebhookParams(webhook_url=webhook_url)
        data = params.model_dump(exclude_none=True)

        return await self._perform_async_request(url, data)

    def parse_updates(self, response: dict) -> List[Update]:
        """
        Парсинг ответа getUpdates в список Update объектов.

        Args:
            response: dict ответ от getUpdates

        Returns:
            List[Update]
        """
        if response.get("ok") and "updates" in response:
            return [Update.model_validate(update) for update in response["updates"]]
        return []
