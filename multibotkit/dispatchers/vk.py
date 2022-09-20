from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.vk.incoming import IncomingEvent


class VkontakteDispatcher(BaseDispatcher):
    async def process_event(
        self, event: IncomingEvent
    ):
        sender_id = event.object.message.from_id
        state_id = f"vkontakte_{sender_id}"
        state_object = await self.state_manager.get_state(state_id)

        for (func, state_func, handler) in self._handlers:
            
            state_func_result = True
            if state_func is not None:
                try:
                    state_func_result = state_func(state_object)
                except Exception:
                    continue
            
            func_result = True
            if func is not None:
                if event.object is None:
                    continue
                try:
                    func_result = func(event)
                except Exception:
                    continue

            summary_result = state_func_result * func_result

            if summary_result:
                await handler(event, state_object)

                if self.logger:
                    new_state_object = await self.state_manager.get_state(state_id)
                    event_log = {
                        "user_id": state_object.id,
                        "paltform": "Vkontakte",
                        "old_state": state_object.state,
                        "old_state_data": state_object.data,
                        "new_state": new_state_object.state,
                        "new_state_data": new_state_object.data,
                        "event": event.dict()
                    }
                    if callable(self.logger):
                        await self.logger(event_log)
                        return
                    self.logger.info(f"Incoming Vkontakte event: {event_log}")
                return
