# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, date_diff, getdate, flt


class ComplianceTask(Document):
    website = frappe._dict(
        route_field='route',
    )
    def validate(self):
        self.set_penalty_risk()

    def set_penalty_risk(self):
        """Auto-calculate penalty risk based on overdue days × penalty_per_day from template."""
        calculate_penalty_risk(self, method=None)


def calculate_penalty_risk(doc, method):
    """Hook function: calculate penalty risk on save."""
    if doc.status != "Filed" and doc.due_date and getdate(today()) > getdate(doc.due_date):
        days_overdue = date_diff(today(), doc.due_date)
        penalty_per_day = 0
        if doc.template:
            penalty_per_day = flt(
                frappe.db.get_value("Compliance Task Template", doc.template, "penalty_per_day")
            )
        doc.penalty_risk = days_overdue * penalty_per_day
    else:
        doc.penalty_risk = 0
