import sentry_sdk

from multibotkit.config import settings
from multibotkit.schemas.telegram.incoming import Update


class TelegramDispatcher:
    """
    Basic dispatcher for Telegram Bot Events
    """
    def __init__(self):
        self.__handlers = []
        self.__default_handler = None
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.SENTRY_ENVIRONMENT,
            server_name=settings.SENTRY_SERVER,
        )


    def handler(
        self,
        func=None,
        state_data_func=None,
    ):
        def wrapper(f):
            self.__handlers.append(
                (
                    func,
                    state_data_func,
                    f,
                )
            )

        return wrapper


    def default_handler(self):
        def wrapper(f):
            self.__default_handler = f

        return wrapper


    async def process_event(self, event: Update, state_data: dict):
        for (
            func,
            state_data_func,
            handler,
        ) in self.__handlers:
            state_data_func_result = None
            if state_data_func is not None:
                state_data_func_result = state_data_func(state_data)

            func_result = None
            if func is not None:
                try:
                    func_result = func(event)
                except Exception:
                    func_result = False
            event_result = {
                state_data_func_result,
                func_result,
            }
            try:
                event_result.remove(None)
            except KeyError:
                pass
            try:
                summary_result = event_result.pop()
                for result in event_result:
                    summary_result *= result
                if summary_result:
                    await handler(event, state_data)
                    return
            except KeyError:
                pass
        if self.__default_handler is not None:
            await self.__default_handler(event, state_data)
