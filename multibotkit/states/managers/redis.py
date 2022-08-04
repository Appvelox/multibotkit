import json
from typing import Optional

import aioredis

from multibotkit.states.managers.base import BaseStateManager


class RedisStateManager(BaseStateManager):

    def __init__(
        self,
        connection_url: str,
        db_number: int = 1
    ):
        self.connection_url = connection_url
        self.db_number = db_number
        self.db = aioredis.from_url(
            self.connection_url, db=self.db_number, decode_responses=True
        )


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
        
        state_to_redis = json.dumps(input_state)
        
        await self.db.set(state_id, state_to_redis)


    async def get_state(self, state_id: str):
        json_doc = await self.db.get(state_id)

        if json_doc is None:
            doc = None
        else:
            doc = json.loads(json_doc)
        
        state = super().get_state(state_id=state_id, doc=doc)
        return state


    async def delete_state(self, state_id: str):
        await self.db.delete(state_id)
