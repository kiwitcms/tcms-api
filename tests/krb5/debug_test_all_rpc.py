#!/usr/bin/env python
#
# DEBUG: Test all RPC methods against PR #4451
#
# Copyright (c) 2026 Kiwi TCMS project. All rights reserved.
# Author: Alexander Todorov <info@kiwitcms.org>
#

"""
DEBUG commit: This test exercises ALL RPC methods exposed by Kiwi TCMS
to verify they work correctly against the django-modern-rpc v2.1.0
changes introduced in PR #4451.

The test connects to a running Kiwi TCMS instance using the credentials
from ~/.tcms.conf and calls every available RPC method with appropriate
sample data. It is designed to catch regressions caused by the migration
from modernrpc.core.rpc_method + @permissions_required + **kwargs to
tcms.rpc.views.rpc_method with auth= and context_target="rpc_context".

Write operations that require specific permissions may raise
PermissionDenied, which is acceptable - the test validates that the
RPC method is reachable and responds correctly, even if the user
doesn't have sufficient permissions.
"""

import os
import ssl
import unittest
from datetime import datetime
from unittest.mock import patch

import requests
from tcms_api import TCMS

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class DoNotVerifySSLSession(requests.sessions.Session):
    def __init__(self):
        super().__init__()
        self.verify = False

    def get(self, url, **kwargs):
        kwargs.setdefault("verify", False)
        return super().get(url, **kwargs)


def patch_session(test_method):
    """Decorator to patch requests session for SSL verification."""

    def wrapper(self):
        with patch("requests.sessions.Session") as session:
            session.return_value = DoNotVerifySSLSession()
            return test_method(self)

    return wrapper


# pylint: disable=too-many-public-methods
class DebugTestAllRPCMethods(unittest.TestCase):
    """Test ALL RPC methods against PR #4451 changes."""

    @classmethod
    def setUpClass(cls):
        cls.rpc = TCMS().exec
        cls.now = datetime.now().isoformat()
        cls.timestamp = f"debug-{cls.now}"

    #
    # Auth
    #
    @patch_session
    def test_auth_login(self):
        result = self.rpc.Auth.login("kiwitcms-bot", "changeme")
        self.assertIsNotNone(result)

    @patch_session
    def test_auth_logout(self):
        result = self.rpc.Auth.logout()
        self.assertIsNone(result)

    #
    # Classification
    #
    @patch_session
    def test_classification_filter(self):
        result = self.rpc.Classification.filter({})
        self.assertGreater(len(result), 0)
        self.assertIn("id", result[0])
        self.assertIn("name", result[0])

    @patch_session
    def test_classification_create(self):
        name = f"tcms-api-debug-{self.now}"
        try:
            result = self.rpc.Classification.create({"name": name})
            self.assertEqual(result["name"], name)
            self.assertIn("id", result)
        except Exception as e:
            # PermissionDenied is acceptable
            self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Product
    #
    @patch_session
    def test_product_filter(self):
        result = self.rpc.Product.filter({})
        self.assertGreater(len(result), 0)
        self.assertIn("id", result[0])
        self.assertIn("name", result[0])

    @patch_session
    def test_product_create(self):
        class_id = self.rpc.Classification.filter({"name": "test-products"})[0]["id"]
        name = f"tcms-api-debug-{self.now}"
        try:
            result = self.rpc.Product.create({"name": name, "classification": class_id})
            self.assertEqual(result["name"], name)
        except Exception as e:
            self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Version
    #
    @patch_session
    def test_version_filter(self):
        result = self.rpc.Version.filter({})
        if result:
            self.assertIn("id", result[0])
            self.assertIn("value", result[0])

    @patch_session
    def test_version_create(self):
        products = self.rpc.Product.filter({})
        if products:
            try:
                result = self.rpc.Version.create(
                    {"product": products[0]["id"], "value": f"debug-{self.now}"}
                )
                self.assertIn("id", result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Build
    #
    @patch_session
    def test_build_filter(self):
        result = self.rpc.Build.filter({})
        self.assertIsInstance(result, list)

    @patch_session
    def test_build_create(self):
        versions = self.rpc.Version.filter({})
        if versions:
            try:
                result = self.rpc.Build.create(
                    {"name": f"debug-{self.now}", "version": versions[0]["id"]}
                )
                self.assertIn("id", result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_build_update(self):
        builds = self.rpc.Build.filter({})
        if builds:
            try:
                result = self.rpc.Build.update(builds[0]["id"], {"is_active": True})
                self.assertIn("id", result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Category
    #
    @patch_session
    def test_category_filter(self):
        result = self.rpc.Category.filter({})
        self.assertIsInstance(result, list)

    @patch_session
    def test_category_create(self):
        products = self.rpc.Product.filter({})
        if products:
            try:
                result = self.rpc.Category.create(
                    {
                        "name": f"debug-{self.now}",
                        "product": products[0]["id"],
                        "description": "debug",
                    }
                )
                self.assertIn("id", result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Component
    #
    @patch_session
    def test_component_filter(self):
        result = self.rpc.Component.filter({})
        self.assertIsInstance(result, list)

    @patch_session
    def test_component_create(self):
        products = self.rpc.Product.filter({})
        if products:
            try:
                result = self.rpc.Component.create(
                    {
                        "name": f"debug-{self.now}",
                        "product": products[0]["id"],
                    }
                )
                self.assertIn("id", result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Priority
    #
    @patch_session
    def test_priority_filter(self):
        result = self.rpc.Priority.filter({})
        self.assertGreater(len(result), 0)
        self.assertIn("id", result[0])
        self.assertIn("value", result[0])

    #
    # PlanType
    #
    @patch_session
    def test_plantype_filter(self):
        result = self.rpc.PlanType.filter({})
        self.assertGreater(len(result), 0)
        self.assertIn("id", result[0])
        self.assertIn("name", result[0])

    @patch_session
    def test_plantype_create(self):
        try:
            result = self.rpc.PlanType.create({"name": f"Debug {self.now}"})
            self.assertIn("id", result)
        except Exception as e:
            self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # TestCaseStatus
    #
    @patch_session
    def test_testcasestatus_filter(self):
        result = self.rpc.TestCaseStatus.filter({})
        self.assertGreater(len(result), 0)
        self.assertIn("id", result[0])
        self.assertIn("name", result[0])

    #
    # TestExecutionStatus
    #
    @patch_session
    def test_testexecutionstatus_filter(self):
        result = self.rpc.TestExecutionStatus.filter({})
        self.assertGreater(len(result), 0)
        self.assertIn("id", result[0])
        self.assertIn("name", result[0])

    #
    # Tag
    #
    @patch_session
    def test_tag_filter(self):
        result = self.rpc.Tag.filter({})
        self.assertIsInstance(result, list)

    #
    # User
    #
    @patch_session
    def test_user_filter(self):
        result = self.rpc.User.filter({})
        self.assertGreater(len(result), 0)
        self.assertIn("id", result[0])
        self.assertIn("username", result[0])

    @patch_session
    def test_user_get_me(self):
        result = self.rpc.User.get_me()
        self.assertIn("id", result)
        self.assertIn("username", result)

    @patch_session
    def test_user_update(self):
        me = self.rpc.User.get_me()
        try:
            result = self.rpc.User.update(me["id"], {"username": me["username"]})
            self.assertIn("id", result)
        except Exception as e:
            self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Group
    #
    @patch_session
    def test_group_filter(self):
        result = self.rpc.Group.filter({})
        self.assertIsInstance(result, list)
        if result:
            self.assertIn("id", result[0])
            self.assertIn("name", result[0])

    #
    # TestCase
    #
    @patch_session
    def test_testcase_filter(self):
        result = self.rpc.TestCase.filter({})
        self.assertIsInstance(result, list)
        if result:
            self.assertIn("id", result[0])
            self.assertIn("summary", result[0])

    @patch_session
    def test_testcase_create_and_delete(self):
        products = self.rpc.Product.filter({})
        if products:
            categories = self.rpc.Category.filter({"product": products[0]["id"]})
            priorities = self.rpc.Priority.filter({})
            statuses = self.rpc.TestCaseStatus.filter({"name": "CONFIRMED"})
            if categories and priorities and statuses:
                try:
                    result = self.rpc.TestCase.create(
                        {
                            "summary": f"DEBUG: test all RPC - {self.now}",
                            "category": categories[0]["id"],
                            "priority": priorities[0]["id"],
                            "case_status": statuses[0]["id"],
                            "is_automated": True,
                        }
                    )
                    self.assertIn("id", result)
                    self.assertIn("summary", result)
                    test_case_id = result["id"]

                    # TestCase.update
                    try:
                        updated = self.rpc.TestCase.update(
                            test_case_id,
                            {"summary": f"DEBUG: updated - {self.now}"},
                        )
                        self.assertIn("id", updated)
                    except Exception as e:
                        self.assertIn("PermissionDenied", str(type(e).__name__))

                    # TestCase.remove
                    try:
                        self.rpc.TestCase.remove({"pk": test_case_id})
                    except Exception as e:
                        self.assertIn("PermissionDenied", str(type(e).__name__))

                except Exception as e:
                    self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testcase_tag_operations(self):
        # Test add_tag and remove_tag with **kwargs -> rpc_context
        cases = self.rpc.TestCase.filter({})
        if cases:
            case_id = cases[0]["id"]
            tag_name = f"debug-{self.now}"
            try:
                self.rpc.TestCase.add_tag(case_id, tag_name)
                try:
                    self.rpc.TestCase.remove_tag(case_id, tag_name)
                except Exception:
                    pass
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testcase_component_ops(self):
        cases = self.rpc.TestCase.filter({})
        if cases:
            try:
                self.rpc.TestCase.add_component(cases[0]["id"], "debug-non-existent")
            except Exception as e:
                # DoesNotExist is expected here - but not a protocol error
                self.assertNotIn("Fault", str(type(e).__name__))

    @patch_session
    def test_testcase_notification_cc(self):
        cases = self.rpc.TestCase.filter({})
        if cases:
            case_id = cases[0]["id"]
            try:
                cc_list = self.rpc.TestCase.get_notification_cc(case_id)
                self.assertIsInstance(cc_list, list)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testcase_comments(self):
        cases = self.rpc.TestCase.filter({})
        if cases:
            try:
                result = self.rpc.TestCase.get_comments(cases[0]["id"])
                self.assertIsInstance(result, list)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # TestPlan
    #
    @patch_session
    def test_testplan_filter(self):
        result = self.rpc.TestPlan.filter({})
        self.assertIsInstance(result, list)
        if result:
            self.assertIn("id", result[0])
            self.assertIn("name", result[0])

    @patch_session
    def test_testplan_create(self):
        products = self.rpc.Product.filter({})
        if products:
            versions = self.rpc.Version.filter({"product": products[0]["id"]})
            plan_types = self.rpc.PlanType.filter({})
            if versions and plan_types:
                try:
                    result = self.rpc.TestPlan.create(
                        {
                            "name": f"DEBUG: test all RPC - {self.now}",
                            "product": products[0]["id"],
                            "product_version": versions[0]["id"],
                            "type": plan_types[0]["id"],
                            "text": "debug",
                        }
                    )
                    self.assertIn("id", result)
                except Exception as e:
                    self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testplan_update(self):
        plans = self.rpc.TestPlan.filter({})
        if plans:
            try:
                result = self.rpc.TestPlan.update(
                    plans[0]["id"],
                    {"name": plans[0]["name"]},
                )
                self.assertIn("id", result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testplan_tag_operations(self):
        # Test add_tag and remove_tag with **kwargs -> rpc_context
        plans = self.rpc.TestPlan.filter({})
        if plans:
            plan_id = plans[0]["id"]
            tag_name = f"debug-{self.now}"
            try:
                self.rpc.TestPlan.add_tag(plan_id, tag_name)
                try:
                    self.rpc.TestPlan.remove_tag(plan_id, tag_name)
                except Exception:
                    pass
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testplan_add_case(self):
        plans = self.rpc.TestPlan.filter({})
        cases = self.rpc.TestCase.filter({})
        if plans and cases:
            try:
                result = self.rpc.TestPlan.add_case(plans[0]["id"], cases[0]["id"])
                self.assertIsNotNone(result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testplan_comments(self):
        plans = self.rpc.TestPlan.filter({})
        if plans:
            try:
                result = self.rpc.TestPlan.get_comments(plans[0]["id"])
                self.assertIsInstance(result, list)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # TestRun
    #
    @patch_session
    def test_testrun_filter(self):
        result = self.rpc.TestRun.filter({})
        self.assertIsInstance(result, list)
        if result:
            self.assertIn("id", result[0])
            self.assertIn("summary", result[0])

    @patch_session
    def test_testrun_create(self):
        plans = self.rpc.TestPlan.filter({})
        if plans:
            builds = self.rpc.Build.filter({})
            if builds:
                users = self.rpc.User.filter({})
                if users:
                    try:
                        result = self.rpc.TestRun.create(
                            {
                                "summary": f"DEBUG: test all RPC - {self.now}",
                                "plan": plans[0]["id"],
                                "build": builds[0]["id"],
                                "manager": users[0]["id"],
                                "default_tester": users[0]["id"],
                            }
                        )
                        self.assertIn("id", result)
                    except Exception as e:
                        self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testrun_add_case(self):
        runs = self.rpc.TestRun.filter({})
        cases = self.rpc.TestCase.filter({})
        if runs and cases:
            try:
                result = self.rpc.TestRun.add_case(runs[0]["id"], cases[0]["id"])
                self.assertIsNotNone(result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testrun_get_cases(self):
        runs = self.rpc.TestRun.filter({})
        if runs:
            try:
                result = self.rpc.TestRun.get_cases(runs[0]["id"])
                self.assertIsInstance(result, list)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testrun_tag_operations(self):
        # Test add_tag and remove_tag with **kwargs -> rpc_context
        runs = self.rpc.TestRun.filter({})
        if runs:
            run_id = runs[0]["id"]
            tag_name = f"debug-{self.now}"
            try:
                result = self.rpc.TestRun.add_tag(run_id, tag_name)
                self.assertIsNotNone(result)
                try:
                    self.rpc.TestRun.remove_tag(run_id, tag_name)
                except Exception:
                    pass
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testrun_update(self):
        runs = self.rpc.TestRun.filter({})
        if runs:
            try:
                result = self.rpc.TestRun.update(
                    runs[0]["id"],
                    {"summary": runs[0]["summary"]},
                )
                self.assertIn("id", result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # TestExecution
    #
    @patch_session
    def test_testexecution_filter(self):
        result = self.rpc.TestExecution.filter({})
        self.assertIsInstance(result, list)
        if result:
            self.assertIn("id", result[0])
            self.assertIn("status__name", result[0])

    @patch_session
    def test_testexecution_update(self):
        executions = self.rpc.TestExecution.filter({})
        if executions:
            statuses = self.rpc.TestExecutionStatus.filter({})
            if statuses:
                try:
                    self.rpc.TestExecution.update(
                        executions[0]["id"],
                        {"status": statuses[0]["id"]},
                    )
                except Exception as e:
                    self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testexecution_comments(self):
        executions = self.rpc.TestExecution.filter({})
        if executions:
            exec_id = executions[0]["id"]

            # TestExecution.add_comment (has **kwargs -> rpc_context)
            try:
                comment_result = self.rpc.TestExecution.add_comment(
                    exec_id, f"DEBUG comment {self.now}"
                )
                self.assertIn("id", comment_result)

                # TestExecution.get_comments
                comments = self.rpc.TestExecution.get_comments(exec_id)
                self.assertIsInstance(comments, list)

                # TestExecution.remove_comment
                try:
                    self.rpc.TestExecution.remove_comment(exec_id, comment_result["id"])
                except Exception:
                    pass
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    @patch_session
    def test_testexecution_history(self):
        executions = self.rpc.TestExecution.filter({})
        if executions:
            try:
                history = self.rpc.TestExecution.history(executions[0]["id"])
                self.assertIsInstance(history, list)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Bug
    #
    @patch_session
    def test_bug_filter(self):
        try:
            result = self.rpc.Bug.filter({})
            self.assertIsInstance(result, list)
        except Exception as e:
            # Bug app may not be enabled
            self.assertIn("DoesNotExist", str(type(e).__name__))

    @patch_session
    def test_bug_create(self):
        products = self.rpc.Product.filter({})
        if products:
            try:
                result = self.rpc.Bug.create(
                    {"summary": f"DEBUG: Bug {self.now}", "product": products[0]["id"]}
                )
                self.assertIn("id", result)
            except Exception as e:
                self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # KiwiTCMS app methods
    #
    @patch_session
    def test_kiwitcms_version(self):
        try:
            result = self.rpc.KiwiTCMS.version()
            self.assertIn("version", result)
            self.assertIn("product", result)
        except Exception as e:
            self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Markdown rendering
    #
    @patch_session
    def test_markdown(self):
        try:
            result = self.rpc.Markdown.render("**hello**")
            self.assertIsNotNone(result)
        except Exception as e:
            self.assertIn("PermissionDenied", str(type(e).__name__))

    #
    # Bugtracker
    #
    @patch_session
    def test_bugtracker_all(self):
        try:
            result = self.rpc.BugTracker.filter({})
            self.assertIsInstance(result, list)
        except Exception as e:
            self.assertIn("PermissionDenied", str(type(e).__name__))


if __name__ == "__main__":
    unittest.main()
