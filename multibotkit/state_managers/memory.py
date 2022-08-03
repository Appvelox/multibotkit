from typing import Optional

from multibotkit.state_managers.base import BaseStateManager


class MemoryStateManager(BaseStateManager):

    def __init__(self):
        self.storage = {}


    async def set_state(
        self,
        state_id: str,
        state: Optional[str] = None,
        state_data: Optional[dict] = None
    ):

        input_state = await super().set_state(
            state_id=state_id,
            state=state,
            state_data=state_data
        )

        self.storage[state_id] = input_state


    async def get_state(self, state_id: str):
        
        if state_id not in self.storage.keys():
            doc = None
        else:
            doc = self.storage[state_id]
        
        state = super().get_state(state_id=state_id, doc=doc)
        return state


    async def delete_state(self, state_id: str):
        self.storage.pop(state_id)