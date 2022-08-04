from typing import Optional

from multibotkit.states.state import State


class BaseStateManager():
   
    def create_State(self, state_id: str, state: str, data: dict = {}):
        return State(self, state_id, state, data)


    def get_state(self, state_id: str, doc: Optional[dict]):
        
        if doc is None:
            state = self.create_State(
                state_id=state_id,
                state=None,
                data=None
            )
            return state
        
        state = self.create_State(
            state_id=state_id,
            state=doc["state"],
            data=doc["data"]
        )
        return state


    async def set_state(
        self,
        state_id: str,
        state: Optional[str] = None,
        state_data: Optional[dict] = None
    ):
        state_object = await self.get_state(state_id=state_id)
        
        if state is None:
            state = state_object.state
        if state_data is None:
            state_data = state_object.data
        
        input_state = {
            "state": state,
            "data": state_data
        }

        return input_state
