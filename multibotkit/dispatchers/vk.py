from typing import Callable
from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.vk.incoming import IncomingEvent


class VkontakteDispatcher(BaseDispatcher):
    
    @BaseDispatcher.process_event_decorator
    async def process_event(
        self,
        event: IncomingEvent,
        state_data: dict,
        func: Callable = None
    ):
        if func is not None:
            func_result = False
            if event.object is not None:
                try:
                    func_result = func(event)
                except Exception:
                    func_result = False
        
        return func_result
