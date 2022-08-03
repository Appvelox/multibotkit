from typing import Optional


class BaseStateManager():

    class State():
        def __init__(self, manager, state_id: str, state: str, data: dict):
            self.id = state_id
            self.state = state
            self.data = data
            self.manager = manager
        
        async def set_state(self, state: str, data: Optional[dict] = None):
            new_data = self.data if data is None else data
            await self.manager.set_state(
                state_id=self.id,
                state=state,
                state_data=new_data
            )
        
        async def delete_state(self):
            await self.manager.delete_state(state_id=self.id)

   
    def create_State(self, state_id: str, state: str, data: dict = {}):
        return self.State(self, state_id, state, data)


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
