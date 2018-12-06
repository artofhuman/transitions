from unittest import TestCase
import asyncio
from unittest.mock import MagicMock

from transitions.extensions.asyncio import AsyncMachine

async def await_false():
    await asyncio.sleep(0.1)
    return False
async def await_true():
    await asyncio.sleep(0.1)
    return True

class TestAsync(TestCase):

    def setUp(self):
        self.machine = AsyncMachine(states=['A', 'B', 'C'], transitions=[['go', 'A', 'B']], initial='A')

    def test_async_machine_cb(self):
        mock = MagicMock()

        async def async_process():
            await asyncio.sleep(0.1)
            mock()

        m = self.machine
        m.after_state_change = async_process
        m.go()
        self.assertEqual(m.state, 'B')
        self.assertTrue(mock.called)

    def test_async_condition_cb(self):
        m = self.machine
        m.add_transition('proceed', 'A', 'C',  conditions=await_true, unless=await_false)
        m.proceed()
        self.assertEqual(m.state, 'C')

    def test_sync_conditions_cb(self):
        mock = MagicMock()

        def sync_process():
            mock()

        m = self.machine
        m.after_state_change = sync_process
        m.go()
        self.assertEqual(m.state, 'B')
        self.assertTrue(mock.called)