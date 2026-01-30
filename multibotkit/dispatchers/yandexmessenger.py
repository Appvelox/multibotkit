import inspect
from datetime import datetime

from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.yandexmessenger.incoming import Update


class YandexMessengerDispatcher(BaseDispatcher):
    """
    Dispatcher для обработки событий Yandex Messenger.

    Логика работы:
    1. Получает Update событие
    2. Определяет sender_id (из login или id)
    3. Загружает/создает state объект для пользователя
    4. Проходит по зарегистрированным handlers
    5. Выполняет handler если условия (func + state_object_func) выполнены
    6. Логирует событие если logger настроен
    """

    async def process_event(self, event: Update):
        """
        Обработка входящего события Update.

        Args:
            event: Update объект с входящим сообщением
        """
        # 1. Определение sender_id
        sender = event.from_
        if sender.login:
            sender_id = sender.login
        elif sender.id:
            sender_id = sender.id
        else:
            sender_id = "unknown"  # fallback

        # 2. Формирование state_id
        # ВАЖНО: использовать "yandexmessenger" (одно слово)
        # чтобы state.id = state_id.split("_")[1] работало корректно
        state_id = f"yandexmessenger_{sender_id}"
        state_object = await self.state_manager.get_state(state_id)

        # 3. Обработка handlers
        for (func, state_func, handler) in self._handlers:
            state_func_result = True
            if state_func is not None:
                try:
                    if inspect.iscoroutinefunction(state_func):
                        state_func_result = await state_func(state_object)
                    else:
                        state_func_result = state_func(state_object)
                except Exception:
                    continue

            func_result = True
            if func is not None:
                try:
                    if inspect.iscoroutinefunction(func):
                        func_result = await func(event)
                    else:
                        func_result = func(event)
                except Exception:
                    continue

            summary_result = state_func_result * func_result

            if summary_result:
                await handler(event, state_object)

                # 4. Логирование
                if self.logger:
                    new_state_object = await self.state_manager.get_state(state_id)
                    event_log = {
                        "created_at": datetime.now(),
                        "user_id": state_object.id,
                        "platform": "YandexMessenger",
                        "old_state": state_object.state,
                        "old_state_data": state_object.data,
                        "new_state": new_state_object.state,
                        "new_state_data": new_state_object.data,
                        "event": event.dict(),
                    }
                    if callable(self.logger):
                        await self.logger(event_log)
                        return
                    self.logger.info(f"Incoming YandexMessenger event: {event_log}")
                return
