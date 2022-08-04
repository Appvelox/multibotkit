from typing import Callable, Optional
from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.vk.incoming import IncomingEvent


class VkontakteDispatcher(BaseDispatcher):
    
    def __getting_func_result(
        self,
        event: IncomingEvent,
        func: Optional[Callable] = None
    ):
        if func is not None:
            func_result = False
            if event.object is not None:
                try:
                    func_result = func(event)
                except Exception:
                    func_result = False
        
        return func_result
    
    async def process_event(
            self,
            event: IncomingEvent,
            func: Optional[Callable] = None,
        ):

        await super().process_event(event, func)
