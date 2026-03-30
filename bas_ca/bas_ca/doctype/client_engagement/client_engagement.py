# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ClientEngagement(Document):
    website = frappe._dict(
        condition_field='portal_access',
        route_field='route',
    )
    def validate(self):
        self.validate_pan()
        self.validate_gstin()

    def validate_pan(self):
        if self.pan and len(self.pan) != 10:
            frappe.throw("PAN must be exactly 10 characters")

    def validate_gstin(self):
        if self.gstin and len(self.gstin) != 15:
            frappe.throw("GSTIN must be exactly 15 characters")
