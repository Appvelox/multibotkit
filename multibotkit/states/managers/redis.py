import json
from typing import Optional

import aioredis

from multibotkit.states.managers.base import BaseStateManager
from multibotkit.states.state import State


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
        state_data: Optional[dict] = None,
    ):
        state_object = await self.get_state(state_id=state_id)

        if state is None:
            state = state_object.state
        if state_data is None:
            state_data = state_object.data

        input_state = {"state": state, "data": state_data}

        state_to_redis = json.dumps(input_state)

        await self.db.set(state_id, state_to_redis)


    async def get_state(
        self, state_id: str
    ):
        json_doc = await self.db.get(state_id)

        if json_doc is None:
            state = State(
                self,
                state_id=state_id,
                state=None,
                state_data=None
            )
            return state

        doc = json.loads(json_doc)

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
        await self.db.delete(state_id)
