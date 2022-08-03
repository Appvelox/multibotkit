from typing import Callable

from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.viber.incoming import Callback


class ViberDispatcher(BaseDispatcher):
    
    @BaseDispatcher.process_event_decorator
    async def process_event(
        self,
        event: Callback,
        func: Callable = None
    ):
        if func is not None:
            try:
                func_result = func(event)
            except Exception:
                func_result = False
        
        return func_result
