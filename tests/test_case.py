from unittest.mock import MagicMock

from . import PluginTestCase


class GivenTestCaseExistsInDatabase(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend.rpc = MagicMock()
        cls.backend.rpc.TestCase.filter = MagicMock(return_value=[{"case_id": 34}])
        cls.backend.rpc.TestCase.create = MagicMock()

    def test_when_test_case_get_or_create_then_reuses_it(self):
        test_case, created = self.backend.test_case_get_or_create("Automated test case")
        self.assertEqual(test_case["case_id"], 34)
        self.assertFalse(created)
        self.backend.rpc.TestCase.create.assert_not_called()


class GivenTestCaseDoesNotExistInDatabase(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend.rpc = MagicMock()
        cls.backend.rpc.TestCase.filter = MagicMock(return_value=[])
        cls.backend.rpc.TestCase.create = MagicMock(return_value={"case_id": 43})
        cls.backend.category_id = 999
        cls.backend.priority_id = 777
        cls.backend.confirmed_id = 666

    def test_when_test_case_get_or_create_then_creates_it(self):
        test_case, created = self.backend.test_case_get_or_create("Automated test case")
        self.assertEqual(test_case["case_id"], 43)
        self.assertTrue(created)
        self.backend.rpc.TestCase.create.assert_called_with(
            {
                "summary": "Automated test case",
                "category": 999,
                "priority": 777,
                "case_status": 666,
                "notes": self.backend.created_by_text,
                "is_automated": True,
            }
        )
