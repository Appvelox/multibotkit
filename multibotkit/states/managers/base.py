from typing import Optional


class BaseStateManager:
    def get_state(self, state_id: str):
        raise NotImplementedError("get_state is not implemented")

    async def set_state(
        self,
        state_id: str,
        state: Optional[str] = None,
        state_data: Optional[dict] = None,
    ):
        raise NotImplementedError("set_state is not implemented")

    def delete_state(self, state_id: str):
        raise NotImplementedError("delete_state is not implemented")
