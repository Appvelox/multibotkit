from typing import Callable, Optional

from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.telegram.incoming import Update


class TelegramDispatcher(BaseDispatcher):
    
    def _getting_func_result(
        self,
        event: Update,
        func: Optional[Callable] = None
    ):
        if func is not None:
            try:
                func_result = func(event)
            except Exception:
                func_result = False
        
        return func_result
