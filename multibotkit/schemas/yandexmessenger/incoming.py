from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatType(str, Enum):
    """Типы чатов в Yandex Messenger"""

    private = "private"
    group = "group"
    channel = "channel"


class Sender(BaseModel):
    """
    Отправитель сообщения.
    Либо login (для пользователей), либо id (для ботов/каналов).
    """

    login: Optional[str] = Field(None, title="Login пользователя")
    id: Optional[str] = Field(None, title="ID отправителя (для ботов/каналов)")
    display_name: Optional[str] = Field(None, title="Отображаемое имя")
    robot: Optional[bool] = Field(None, title="Является ли отправитель роботом")


class Chat(BaseModel):
    """
    Информация о чате.
    Для private чатов id отсутствует.
    """

    type: ChatType = Field(..., title="Тип чата: private/group/channel")
    id: Optional[str] = Field(
        None, title="ID чата (для group/channel, отсутствует для private)"
    )


class Image(BaseModel):
    """Изображение в сообщении"""

    file_id: str = Field(..., title="ID файла для повторного использования")
    width: int = Field(..., title="Ширина изображения в пикселях")
    height: int = Field(..., title="Высота изображения в пикселях")
    size: Optional[int] = Field(
        None, title="Размер файла в байтах (опционально для оригиналов)"
    )
    name: Optional[str] = Field(
        None, title="Имя файла (опционально для оригиналов)"
    )


class File(BaseModel):
    """Файл в сообщении"""

    id: str = Field(..., title="ID файла")
    name: str = Field(..., title="Имя файла")
    size: int = Field(..., title="Размер файла в байтах")


class Update(BaseModel):
    """
    Входящее обновление от Yandex Messenger.
    Соответствует структуре getUpdates response и webhook payload.
    """

    update_id: int = Field(..., title="Уникальный ID обновления")
    message_id: int = Field(..., title="ID сообщения")
    timestamp: int = Field(..., title="Unix timestamp сообщения")
    from_: Sender = Field(..., title="Отправитель сообщения", alias="from")
    chat: Chat = Field(..., title="Информация о чате")
    text: Optional[str] = Field(None, title="Текст сообщения (до 6000 символов)")
    images: Optional[List[Image]] = Field(
        None, title="Массив изображений (если есть)"
    )
    file: Optional[File] = Field(None, title="Прикрепленный файл")

    class Config:
        populate_by_name = True
