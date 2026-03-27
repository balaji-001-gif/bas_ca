# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "client", "label": "Client", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"fieldname": "filing_period", "label": "Period", "fieldtype": "Data", "width": 100},
        {"fieldname": "return_type", "label": "Return Type", "fieldtype": "Data", "width": 100},
        {"fieldname": "total_tax_liability", "label": "Tax Liability (₹)", "fieldtype": "Currency", "width": 140},
        {"fieldname": "itc_claimed", "label": "ITC Claimed (₹)", "fieldtype": "Currency", "width": 130},
        {"fieldname": "itc_as_per_2b", "label": "2B ITC (₹)", "fieldtype": "Currency", "width": 120},
        {"fieldname": "itc_difference", "label": "Difference (₹)", "fieldtype": "Currency", "width": 130},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100},
        {"fieldname": "mismatch_flag", "label": "Mismatch", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    conditions = {}
    if filters:
        if filters.get("financial_year"):
            conditions["financial_year"] = filters.get("financial_year")
        if filters.get("return_type"):
            conditions["return_type"] = filters.get("return_type")
        if filters.get("client_engagement"):
            conditions["client_engagement"] = filters.get("client_engagement")

    records = frappe.get_all(
        "GST Return Tracker",
        filters=conditions,
        fields=[
            "name", "client_engagement", "filing_period", "return_type",
            "total_tax_liability", "itc_claimed", "itc_as_per_2b",
            "itc_difference", "status",
        ],
        order_by="filing_period asc",
    )

    data = []
    for r in records:
        client = frappe.db.get_value(
            "Client Engagement", r.client_engagement, "client"
        ) if r.client_engagement else ""

        mismatch = "⚠️ Mismatch" if abs(flt(r.itc_difference)) > 1000 else "✅ OK"

        data.append({
            "client": client,
            "filing_period": r.filing_period,
            "return_type": r.return_type,
            "total_tax_liability": flt(r.total_tax_liability),
            "itc_claimed": flt(r.itc_claimed),
            "itc_as_per_2b": flt(r.itc_as_per_2b),
            "itc_difference": flt(r.itc_difference),
            "status": r.status,
            "mismatch_flag": mismatch,
        })

    return data
