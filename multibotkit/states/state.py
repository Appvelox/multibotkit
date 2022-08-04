from typing import Optional


class State:
    def __init__(self, manager, state_id: str, state: str, data: dict):
        self.id = state_id
        self.state = state
        self.data = data
        self.manager = manager

    async def set_state(self, state: str, data: Optional[dict] = None):
        new_data = self.data if data is None else data
        await self.manager.set_state(state_id=self.id, state=state, state_data=new_data)

    async def delete_state(self):
        await self.manager.delete_state(state_id=self.id)
