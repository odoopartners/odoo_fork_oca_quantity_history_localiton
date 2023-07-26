# Copyright 2019 ForgeFlow S.L.
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast
from odoo.tests import common
from odoo.exceptions import MissingError

class TestStockQuantityHistory(common.TransactionCase):
    def setUp(self):
        super(TestStockQuantityHistory, self).setUp()
        self.location = self.env["stock.location"].create({"name": "Test Location"})


    def test_open_at_date_without_location(self):
        stock_quantity_history = self.env["stock.quantity.history"].create({
            "include_child_locations": False,
        })

        action = stock_quantity_history.open_at_date()
        ctx = action.get("context")
        self.assertTrue(isinstance(ctx, dict))
        self.assertIsNone(ctx.get("location"))
        self.assertFalse(ctx.get("compute_child", False))


    def test_open_at_date_with_invalid_context(self):
        stock_quantity_history = self.env["stock.quantity.history"].create({
            "location_id": self.location.id,
            "include_child_locations": True,
        })

        stock_quantity_history.open_at_date()["context"] = "Invalid Context"
        action = stock_quantity_history.open_at_date()
        self.assertTrue(isinstance(action.get("context"), dict))
        self.assertEqual(action.get("context").get("location"), self.location.id)
        self.assertTrue(action.get("context").get("compute_child"))



    def test_open_at_date_with_company_owned(self):
        stock_quantity_history = self.env["stock.quantity.history"].create({
            "location_id": self.location.id,
            "include_child_locations": True,
        })
        stock_quantity_history.open_at_date()["context"] = "{'company_owned': True}"
        action = stock_quantity_history.open_at_date()
        ctx = action.get("context")
        self.assertTrue(isinstance(ctx, dict))
        self.assertFalse("company_owned" in ctx)




