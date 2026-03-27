# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff, flt, getdate


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    summary = get_summary(data)
    return columns, data, summary


def get_columns():
    return [
        {"fieldname": "client", "label": "Client", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"fieldname": "form_number", "label": "Form", "fieldtype": "Data", "width": 100},
        {"fieldname": "task_name", "label": "Task", "fieldtype": "Data", "width": 180},
        {"fieldname": "due_date", "label": "Due Date", "fieldtype": "Date", "width": 110},
        {"fieldname": "filing_date", "label": "Filing Date", "fieldtype": "Date", "width": 110},
        {"fieldname": "days_late", "label": "Days Late", "fieldtype": "Int", "width": 90},
        {"fieldname": "penalty_per_day", "label": "Penalty/Day (₹)", "fieldtype": "Currency", "width": 120},
        {"fieldname": "penalty_paid", "label": "Penalty Paid (₹)", "fieldtype": "Currency", "width": 120},
        {"fieldname": "penalty_saved", "label": "Penalty Saved (₹)", "fieldtype": "Currency", "width": 130},
    ]


def get_data(filters):
    conditions = {"status": "Filed"}

    if filters:
        if filters.get("from_date"):
            conditions["due_date"] = [">=", filters.get("from_date")]
        if filters.get("to_date"):
            conditions["due_date"] = ["<=", filters.get("to_date")]

    tasks = frappe.get_all(
        "Compliance Task",
        filters=conditions,
        fields=[
            "name", "client_engagement", "task_name", "form_number",
            "due_date", "filing_date", "template", "penalty_risk",
        ],
        order_by="due_date asc",
    )

    data = []
    for task in tasks:
        client = frappe.db.get_value(
            "Client Engagement", task.client_engagement, "client"
        ) if task.client_engagement else ""

        penalty_per_day = 0
        if task.template:
            penalty_per_day = flt(
                frappe.db.get_value("Compliance Task Template", task.template, "penalty_per_day")
            )

        days_late = 0
        penalty_paid = 0
        if task.filing_date and task.due_date:
            diff = date_diff(task.filing_date, task.due_date)
            if diff > 0:
                days_late = diff
                penalty_paid = days_late * penalty_per_day

        # Penalty saved = max possible penalty (30 days late) - actual penalty
        max_penalty = 30 * penalty_per_day
        penalty_saved = max_penalty - penalty_paid if penalty_paid < max_penalty else 0

        data.append({
            "client": client,
            "form_number": task.form_number,
            "task_name": task.task_name,
            "due_date": task.due_date,
            "filing_date": task.filing_date,
            "days_late": days_late,
            "penalty_per_day": penalty_per_day,
            "penalty_paid": penalty_paid,
            "penalty_saved": penalty_saved,
        })

    return data


def get_summary(data):
    total_saved = sum(d["penalty_saved"] for d in data)
    total_paid = sum(d["penalty_paid"] for d in data)
    return [
        {"label": "Total Penalty Saved", "value": total_saved, "datatype": "Currency"},
        {"label": "Total Penalty Paid", "value": total_paid, "datatype": "Currency"},
        {"label": "Tasks Filed", "value": len(data), "datatype": "Int"},
    ]
