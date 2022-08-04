from typing import Callable, Optional

from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.fb.incoming import IncomingEvent


class FacebookDispatcher(BaseDispatcher):
    async def process_event(
        self, event: IncomingEvent, func: Optional[Callable] = None
    ):

        sender_id = event.entry[0].messaging[0].sender.id
        state_id = f"facebook_{sender_id}"

        state_object = await self.state_manager.get_state(state_id)

        for (func, state_object_func, handler) in self._handlers:
            state_object_func_result = None
            if state_object_func is not None:
                state_object_func_result = state_object_func(state_object)

            if func is not None:
                try:
                    func_result = func(event)
                except Exception:
                    func_result = False

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
        if self._default_handler is not None:
            await self._default_handler(event, state_object)
