from typing import Callable

from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.fb.incoming import IncomingEvent


class FacebookDispatcher(BaseDispatcher):

    @BaseDispatcher.process_event_decorator
    async def process_event(
        self,
        event: IncomingEvent,
        func: Callable = None
    ):
        if func is not None:
            try:
                func_result = func(event)
            except Exception:
                func_result = False
        
        return func_result
