from typing import Optional

from multibotkit.states.managers.base import BaseStateManager


class State:
    def __init__(
        self,
        manager: BaseStateManager,
        state_id: str,
        state: str,
        state_data: dict
    ):
        self.db_id = state_id
        self.id = state_id.split("_")[1]
        self.state = state
        self.data = state_data
        self.manager = manager


    async def set_state(
        self,
        state: Optional[str] = None,
        state_data: Optional[dict] = None
    ):
        new_state = self.state if state is None else state
        new_data = self.data if state_data is None else state_data
        
        await self.manager.set_state(
            state_id=self.db_id,
            state=new_state,
            state_data=new_data
        )


    async def delete_state(self):
        await self.manager.delete_state(state_id=self.db_id)
