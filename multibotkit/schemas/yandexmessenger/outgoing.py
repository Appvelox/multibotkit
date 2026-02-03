from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator

from multibotkit.schemas.yandexmessenger.incoming import Update


class InlineKeyboardButton(BaseModel):
    """Кнопка inline клавиатуры"""

    text: str = Field(..., title="Текст кнопки")
    callback_data: Optional[Union[str, dict]] = Field(
        None, title="JSON данные для callback (автоматически сериализуется)"
    )


class InlineKeyboard(BaseModel):
    """
    Inline клавиатура (до 100 кнопок общего).
    Структура: массив рядов, каждый ряд - массив кнопок.
    """

    buttons: List[InlineKeyboardButton] = Field(..., title="Массив кнопок")

    @field_validator("buttons")
    @classmethod
    def validate_button_count(cls, v: list) -> list:
        """Проверка лимита в 100 кнопок"""
        total_buttons = len(v)
        if total_buttons > 100:
            raise ValueError("Максимум 100 кнопок в клавиатуре")
        return v


class SendTextParams(BaseModel):
    """Параметры для метода sendText"""

    text: str = Field(..., title="Текст сообщения", max_length=6000)
    chat_id: Optional[str] = Field(None, title="ID чата (для групповых чатов)")
    login: Optional[str] = Field(None, title="Login пользователя (для приватных чатов)")
    payload_id: Optional[str] = Field(
        None, title="Уникальный ID для дедупликации (рекомендуется для webhook)"
    )
    reply_message_id: Optional[int] = Field(None, title="ID сообщения для ответа")
    disable_notification: Optional[bool] = Field(None, title="Отключить уведомление")
    important: Optional[bool] = Field(None, title="Отметить сообщение как важное")
    disable_web_page_preview: Optional[bool] = Field(
        None, title="Отключить превью веб-страниц"
    )
    thread_id: Optional[int] = Field(None, title="ID треда для ответа в треде")
    inline_keyboard: Optional[InlineKeyboard] = Field(None, title="Inline клавиатура")

    @model_validator(mode="after")
    def validate_chat_or_login(self):
        """Проверка что указан либо chat_id либо login"""
        if not self.chat_id and not self.login:
            raise ValueError("Необходимо указать либо chat_id либо login")
        return self


class SendImageParams(BaseModel):
    """
    Параметры для метода sendImage.
    Файл передается отдельно через multipart/form-data.
    """

    chat_id: Optional[str] = Field(None, title="ID чата (для групповых чатов)")
    login: Optional[str] = Field(None, title="Login пользователя (для приватных чатов)")
    thread_id: Optional[int] = Field(None, title="ID треда")

    @model_validator(mode="after")
    def validate_chat_or_login(self):
        if not self.chat_id and not self.login:
            raise ValueError("Необходимо указать либо chat_id либо login")
        return self


class SendFileParams(BaseModel):
    """
    Параметры для метода sendFile.
    Файл передается через multipart/form-data с Content-Disposition для имени.
    """

    chat_id: Optional[str] = Field(None, title="ID чата (для групповых чатов)")
    login: Optional[str] = Field(None, title="Login пользователя (для приватных чатов)")
    thread_id: Optional[int] = Field(None, title="ID треда")

    @model_validator(mode="after")
    def validate_chat_or_login(self):
        if not self.chat_id and not self.login:
            raise ValueError("Необходимо указать либо chat_id либо login")
        return self


class GetUpdatesParams(BaseModel):
    """Параметры для метода getUpdates"""

    limit: Optional[int] = Field(
        100,
        title="Количество обновлений (по умолчанию 100, макс 1000)",
        ge=1,
        le=1000,
    )
    offset: Optional[int] = Field(0, title="Смещение для пагинации", ge=0)


class SetWebhookParams(BaseModel):
    """Параметры для метода setWebhook"""

    webhook_url: Optional[str] = Field(
        None, title="URL для webhook (null для отключения)"
    )


class MessageResponse(BaseModel):
    """Стандартный ответ от API после отправки сообщения"""

    ok: bool = Field(..., title="Успешность операции")
    message_id: Optional[int] = Field(None, title="ID созданного сообщения")


class UpdatesResponse(BaseModel):
    """Ответ от метода getUpdates"""

    ok: bool = Field(..., title="Успешность операции")
    updates: List[Update] = Field(..., title="Массив обновлений")
