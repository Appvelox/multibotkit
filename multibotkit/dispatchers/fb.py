from typing import Callable, Optional, Union

from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.fb.incoming import IncomingEvent


class FacebookDispatcher(BaseDispatcher):

    def _getting_func_result(
        self,
        event: IncomingEvent,
        func: Optional[Callable] = None
    ):
        if func is not None:
            try:
                func_result = func(event)
            except Exception:
                func_result = False
        
        return func_result
