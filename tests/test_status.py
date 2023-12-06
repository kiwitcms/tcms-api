# pylint: disable=protected-access

from unittest.mock import MagicMock

from . import PluginTestCase


class GivenStatusCache(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend._statuses = {"PASSED": 1}
        cls.backend.rpc = MagicMock()
        cls.backend.rpc.TestExecutionStatus.filter = MagicMock()

    def test_when_status_in_cache_then_return_from_cache(self):
        self.backend.get_status_id("PASSED")
        self.backend.rpc.TestExecutionStatus.filter.assert_not_called()

    def test_when_status_not_in_cache_then_return_from_cache(self):
        self.backend.get_status_id("FAILED")
        self.backend.rpc.TestExecutionStatus.filter.assert_called_with(
            {
                "name": "FAILED",
            }
        )


class GivenStatusFallback(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend.rpc = MagicMock()
        cls.backend.rpc.TestExecutionStatus.filter.side_effect = [
            IndexError,
            MagicMock(),
        ]

    def test_when_status_not_found_by_name_then_return_by_weight(self):
        self.backend.get_status_id("ERROR")
        self.backend.rpc.TestExecutionStatus.filter.assert_called_with(
            {
                "weight__lt": 0,
            }
        )
