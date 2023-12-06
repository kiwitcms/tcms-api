# pylint: disable=invalid-name, protected-access

import os
from unittest.mock import ANY, MagicMock, patch

from . import PluginTestCase


class Given_TCMS_RUN_ID_IsPresent(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend.rpc = MagicMock()
        cls.backend.rpc.TestRun.create = MagicMock()

    def test_when_get_run_id_then_will_use_it(self):
        with patch.dict(
            os.environ,
            {
                "TCMS_RUN_ID": "532",
            },
            True,
        ):
            run_id = self.backend.get_run_id()
            self.assertEqual(run_id, 532)
            self.backend.rpc.TestRun.create.assert_not_called()


class Given_TCMS_RUN_ID_IsNotPresent(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend.rpc = MagicMock()
        cls.backend.get_product_id = MagicMock(return_value=(44, "p.Test"))
        cls.backend.get_version_id = MagicMock(return_value=(55, "v.Test"))
        cls.backend.get_build_id = MagicMock(return_value=(66, "b.Test"))
        cls.backend.get_plan_id = MagicMock(return_value=77)

        cls.backend.rpc.TestPlan.filter = MagicMock(return_value=[{"author": 88}])
        cls.backend.rpc.TestRun.create = MagicMock(return_value={"id": 99})

    def test_when_get_run_id_then_will_create_TestRun(self):
        with patch.dict(os.environ, {}, True):
            run_id = self.backend.get_run_id()
            self.assertEqual(run_id, 99)
            self.backend.rpc.TestRun.create.assert_called_with(
                {
                    "summary": "[TAP] Results for p.Test, v.Test, b.Test",
                    "manager": 88,
                    "default_tester": 88,
                    "plan": 77,
                    "build": 66,
                    "start_date": ANY,
                }
            )


class GivenEmptyTestRun(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend._cases_in_test_run = {}
        cls.backend.rpc = MagicMock()
        cls.backend.rpc.TestRun.add_case = MagicMock()

    def test_when_add_test_case_to_run_then_TestCase_is_added(self):
        self.backend.add_test_case_to_run(11, 222)
        self.backend.rpc.TestRun.add_case.assert_called_with(222, 11)
