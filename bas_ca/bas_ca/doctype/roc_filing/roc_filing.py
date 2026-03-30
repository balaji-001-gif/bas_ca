import frappe
# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class ROCFiling(Document):
    website = frappe._dict(
        condition_field=None,
        route_field='route',
    )

    pass

    def get_list_context(self, context):
        return {
            "row_template": "bas_ca/bas_ca/doctype/roc_filing/templates/roc_filing_row.html"
        }
