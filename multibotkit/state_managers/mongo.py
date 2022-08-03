from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from multibotkit.state_managers.base import BaseStateManager


class MongoStateManager(BaseStateManager):

    def __init__(
        self,
        connection_url: str,
        db_name: str = "states",
        collection: str = "states"
    ):

        self.connection_url = connection_url
        self.collection = collection
        self.client = AsyncIOMotorClient(connection_url)
        self.db = self.client[db_name]


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

        input_state.update({"state_id": state_id})

        await self.db[self.collection].delete_one({"state_id": state_id})
        
        await self.db[self.collection].insert_one(input_state)


    async def get_state(self, state_id: str):
        doc = await self.db[self.collection].find_one(
            {"state_id": state_id}
        )

        state = super().get_state(state_id=state_id, doc=doc)
        return state


    async def delete_state(self, state_id: str):
        result = await self.db[self.collection].delete_one(
            {"state_id": state_id}
        )
        return result
