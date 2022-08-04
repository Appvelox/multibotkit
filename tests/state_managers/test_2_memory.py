import pytest

from multibotkit.states.managers.memory import MemoryStateManager


@pytest.fixture
def memory_manager():
    test_manager = MemoryStateManager()
    return test_manager


@pytest.mark.asyncio
async def test_memory_manager(memory_manager):
    state_id = "telegram_12"
    state = "some_state"
    state_data = {
        "key": "value"
    }

    state_object = await memory_manager.get_state(state_id=state_id)

    assert state_object.state is None
    assert state_object.data is None

    await memory_manager.set_state(
        state_id=state_id,
        state=state,
        state_data=state_data
    )

    state_object = await memory_manager.get_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == state
    assert state_object.data == state_data

    await memory_manager.set_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == state
    assert state_object.data == state_data

    await memory_manager.delete_state(state_id=state_id)

    state_object = await memory_manager.get_state(state_id=state_id)

    assert state_object.state is None
    assert state_object.data is None

    await memory_manager.set_state(
        state_id=state_id,
        state=state,
        state_data=state_data
    )

    state_object = await memory_manager.get_state(state_id=state_id)

    new_state = "new_state"
    new_data = {
        "new_key": "new_value"
    }

    await state_object.set_state(state=new_state, data=new_data)

    state_object = await memory_manager.get_state(state_id=state_id)

    assert state_object.id == state_id
    assert state_object.state == new_state
    assert state_object.data == new_data
