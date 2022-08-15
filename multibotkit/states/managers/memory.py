from typing import Optional

from multibotkit.states.managers.base import BaseStateManager
from multibotkit.states.state import State


class MemoryStateManager(BaseStateManager):

    def __init__(self):
        self.storage = {}


    async def set_state(
        self,
        state_id: str,
        state: Optional[str] = None,
        state_data: Optional[dict] = None,
    ):
        state_object = await self.get_state(state_id=state_id)

        if state is None:
            state = state_object.state
        if state_data is None:
            state_data = state_object.data

        input_state = {"state": state, "data": state_data}

        self.storage[state_id] = input_state


    async def get_state(
        self, state_id: str
    ):
        if state_id not in self.storage.keys():
            state = State(
                self,
                state_id=state_id,
                state=None,
                state_data=None
            )
            return state

        state = State(
            self,
            state_id=state_id,
            state=self.storage[state_id]["state"],
            state_data=self.storage[state_id]["data"],
        )
        return state


    async def delete_state(self, state_id: str):
        if state_id in self.storage.keys():
            self.storage.pop(state_id)
