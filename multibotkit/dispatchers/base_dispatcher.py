from logging import Logger
from typing import Callable, Optional, Union

from pydantic import BaseModel

from multibotkit.states.managers.base import BaseStateManager
from multibotkit.states.managers.memory import MemoryStateManager


class BaseDispatcher:
    def __init__(
        self,
        state_manager: BaseStateManager = MemoryStateManager(),
        logger: Optional[Union[Logger, Callable]] = None
    ):
        self._handlers = []
        self._default_handler = None
        self.state_manager = state_manager
        self.logger = logger

    def handler(self, func=None, state_object_func=None):
        def wrapper(f):
            self._handlers.append((func, state_object_func, f))

        return wrapper

    async def process_event(self, event: BaseModel, func: Optional[Callable] = None):
        raise NotImplementedError("process_event is not implemented")
