# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class ROCFiling(Document):
    website = frappe._dict(
        condition_field=None,
        route_field='route',
    )
    pass
