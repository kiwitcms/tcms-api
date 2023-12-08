#!/usr/bin/env python

#
# Copyright (c) 2020-2024 Kiwi TCMS project. All rights reserved.
# Author: Alexander Todorov <info@kiwitcms.org>
#

import unittest

from datetime import datetime
from tcms_api import TCMS


class IntegrationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rpc = TCMS().exec

    def test_readonly_filtering_works(self):
        results = self.rpc.Product.filter({})
        self.assertGreater(len(results), 0)

    def test_create_objects_works(self):
        now = datetime.now().isoformat()

        result = self.rpc.Classification.filter(
            {
                "name": "test-products",
            }
        )[0]
        self.assertEqual(result["name"], "test-products")
        classification_id = result["id"]

        product_name = "tcms-api-%s" % now
        result = self.rpc.Product.create(
            {"name": product_name, "classification": classification_id}
        )
        self.assertEqual(result["name"], product_name)


if __name__ == "__main__":
    unittest.main()
