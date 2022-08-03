import pytest

from multibotkit.state_managers.redis import RedisStateManager
from tests.config import settings


@pytest.fixture
def redis_manager():
    test_manager = RedisStateManager(
        connection_url=settings.REDIS_CONNECTION_URL
    )
    return test_manager


@pytest.mark.asyncio
async def test_memory_manager(redis_manager):
    state_id = "telegram_12"
    state = "some_state"
    state_data = {
        "key": "value"
    }

    state_object = await redis_manager.get_state(state_id=state_id)

    assert state_object.state is None
    assert state_object.data is None

    await redis_manager.set_state(
        state_id=state_id,
        state=state,
        state_data=state_data
    )

    state_object = await redis_manager.get_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == state
    assert state_object.data == state_data

    await redis_manager.set_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == state
    assert state_object.data == state_data

    await redis_manager.delete_state(state_id=state_id)

    state_object = await redis_manager.get_state(state_id=state_id)

    assert state_object.state == None
    assert state_object.data == None

    await redis_manager.set_state(
        state_id=state_id,
        state=state,
        state_data=state_data
    )

    state_object = await redis_manager.get_state(state_id=state_id)

    new_state = "new_state"
    new_data = {
        "new_key": "new_value"
    }

    await state_object.set_state(state=new_state, data=new_data)

    state_object = await redis_manager.get_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == new_state
    assert state_object.data == new_data


@pytest.mark.asyncio
async def test_clean_db(redis_manager):
    await redis_manager.db.flushdb()