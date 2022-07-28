from typing import Callable, Optional, Union

from multibotkit.schemas.fb.incoming import IncomingEvent as FBIncomingEvent
from multibotkit.schemas.telegram.incoming import Update
from multibotkit.schemas.viber.incoming import Callback
from multibotkit.schemas.vk.incoming import IncomingEvent as VKIncomingEvent


class BaseDispatcher():
    
    def __init__(self):
        self.__handlers = []
        self.__default_handler = None

    def handler(self, func=None, state_data_func=None):
        def wrapper(f):
            self.__handlers.append((func, state_data_func, f))

        return wrapper

    def default_handler(self):
        def wrapper(f):
            self.__default_handler = f

        return wrapper


    @staticmethod
    def process_event_decorator(getting_func_result: Callable):
        async def wrapper(
            self,
            event: Union[Callback, FBIncomingEvent, Update, VKIncomingEvent],
            state_data: dict,
            func: Optional[Callable] = None
        ):
            for (func, state_data_func, handler) in self.__handlers:
                state_data_func_result = None
                if state_data_func is not None:
                    state_data_func_result = state_data_func(state_data)
                
                func_result = await getting_func_result(self, event, state_data, func)

                event_result = {state_data_func_result, func_result}
                
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
        
        return wrapper
