from typing import Callable, Optional, Union

from multibotkit.schemas.fb.incoming import IncomingEvent as FBIncomingEvent
from multibotkit.schemas.telegram.incoming import Update
from multibotkit.schemas.viber.incoming import Callback
from multibotkit.schemas.vk.incoming import IncomingEvent as VKIncomingEvent
from multibotkit.state_managers.memory import MemoryStateManager
from multibotkit.state_managers.mongo import MongoStateManager
from multibotkit.state_managers.redis import RedisStateManager


class BaseDispatcher():
    
    def __init__(
        self,
        state_manager: Union[
            MemoryStateManager, MongoStateManager, RedisStateManager
        ] = MemoryStateManager()
    ):
        self.__handlers = []
        self.__default_handler = None
        self.state_manager = state_manager


    def handler(self, func=None, state_object_func=None):
        def wrapper(f):
            self.__handlers.append((func, state_object_func, f))

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
            func: Optional[Callable] = None
        ):
            if type(event) == Callback:
                state_id = f"viber_{event.user_id}"
            
            elif type(event) == FBIncomingEvent:
                sender_id = event.entry[0].messaging[0].sender.id
                state_id = f"facebook_{sender_id}"
            
            elif type(event) == Update:
                if event.message is not None:
                    sender_id = event.message.from_.id
                if event.callback_query is not None:
                    sender_id = event.callback_query.from_.id
                state_id = f"telegram_{sender_id}"
            
            elif type(event) == VKIncomingEvent:
                sender_id = event.object.message.from_id
                state_id = f"vkontakte_{sender_id}"
            
            state_object = await self.state_manager.get_state(state_id)
            
            for (func, state_object_func, handler) in self.__handlers:
                state_object_func_result = None
                if state_object_func is not None:
                    state_object_func_result = state_object_func(state_object)
                
                func_result = await getting_func_result(self, event, func)

                event_result = {state_object_func_result, func_result}
                
                try:
                    event_result.remove(None)
                except KeyError:
                    pass
                
                try:
                    summary_result = event_result.pop()
                    for result in event_result:
                        summary_result *= result
                    if summary_result:
                        await handler(event, state_object)
                        return
                except KeyError:
                    pass
            if self.__default_handler is not None:
                await self.__default_handler(event, state_object)
        
        return wrapper
