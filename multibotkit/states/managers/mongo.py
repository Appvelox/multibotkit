from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from multibotkit.states.managers.base import BaseStateManager
from multibotkit.states.state import State


class MongoStateManager(BaseStateManager):
    
    def __init__(
        self, connection_url: str, db_name: str = "states", collection: str = "states"
    ):
        self.connection_url = connection_url
        self.collection = collection
        self.client = AsyncIOMotorClient(connection_url)
        self.db = self.client[db_name]


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

        if state_object.state is not None:
            await self.db[self.collection].update_one(
                {"state_id": state_id}, {"$set": {"state": state, "data": state_data}}
            )
        else:
            await self.db[self.collection].insert_one(
                {"state_id": state_id, "state": state, "data": state_data}
            )


    async def get_state(
        self, state_id: str
    ):
        doc = await self.db[self.collection].find_one({"state_id": state_id})

        if doc is None:
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
            state=doc["state"],
            state_data=doc["data"]
        )
        return state


    async def delete_state(
        self, state_id: str
    ):
        result = await self.db[self.collection].delete_one({"state_id": state_id})
        return result
