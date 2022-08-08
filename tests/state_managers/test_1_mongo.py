import pytest

from multibotkit.states.managers.mongo import MongoStateManager
from tests.config import settings


@pytest.fixture
def mongo_manager():
    test_manager = MongoStateManager(
        connection_url=settings.MONGO_CONNECTION_URL,
        db_name="TEST_DB",
        collection="TEST_COLLECTION",
    )
    return test_manager


@pytest.mark.asyncio
async def test_mongo_manager(mongo_manager):
    state_id = "telegram_12"
    state = "some_state"
    state_data = {"key": "value"}

    state_object = await mongo_manager.get_state(state_id=state_id)

    assert state_object.state is None
    assert state_object.data is None

    await mongo_manager.set_state(state_id=state_id, state=state, state_data=state_data)

    state_object = await mongo_manager.get_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == state
    assert state_object.data == state_data

    await mongo_manager.set_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == state
    assert state_object.data == state_data

    await mongo_manager.delete_state(state_id=state_id)

    state_object = await mongo_manager.get_state(state_id=state_id)

    assert state_object.state is None
    assert state_object.data is None

    await mongo_manager.set_state(state_id=state_id, state=state, state_data=state_data)

    state_object = await mongo_manager.get_state(state_id=state_id)

    new_state = "new_state"
    new_data = {"new_key": "new_value"}

    await state_object.set_state(state=new_state, data=new_data)

    state_object = await mongo_manager.get_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == new_state
    assert state_object.data == new_data


@pytest.mark.asyncio
async def test_clean_db(mongo_manager):
    await mongo_manager.db[mongo_manager.collection].delete_many({})
