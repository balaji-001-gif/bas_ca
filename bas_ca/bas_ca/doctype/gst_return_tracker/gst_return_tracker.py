# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class GSTReturnTracker(Document):
    website = frappe._dict(
        route_field='route',
    )
    def validate(self):
        self.calculate_itc_diff()

    def calculate_itc_diff(self):
        """Auto-calculate ITC difference and flag mismatches."""
        calculate_itc_difference(self, method=None)


def calculate_itc_difference(doc, method):
    """Hook function: calculate ITC difference and flag mismatches on save."""
    doc.itc_difference = flt(doc.itc_as_per_2b) - flt(doc.itc_claimed)
    if abs(flt(doc.itc_difference)) > 1000:
        frappe.msgprint(
            f"⚠️ ITC Mismatch detected: Difference of ₹{doc.itc_difference:,.2f}",
            alert=True,
            indicator="orange",
        )
        # Add comment for audit trail
        if not doc.is_new():
            doc.add_comment(
                "Comment",
                f"⚠️ ITC Mismatch detected: ITC as per 2B (₹{flt(doc.itc_as_per_2b):,.2f}) "
                f"- ITC Claimed (₹{flt(doc.itc_claimed):,.2f}) = ₹{flt(doc.itc_difference):,.2f}",
            )
