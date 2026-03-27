# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, date_diff, getdate, flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {"fieldname": "client", "label": "Client", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"fieldname": "task_name", "label": "Task", "fieldtype": "Data", "width": 200},
        {"fieldname": "form_number", "label": "Form", "fieldtype": "Data", "width": 100},
        {"fieldname": "compliance_type", "label": "Type", "fieldtype": "Data", "width": 120},
        {"fieldname": "due_date", "label": "Due Date", "fieldtype": "Date", "width": 110},
        {"fieldname": "days_overdue", "label": "Days Overdue", "fieldtype": "Int", "width": 110},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100},
        {"fieldname": "assigned_to", "label": "Assigned To", "fieldtype": "Link", "options": "User", "width": 150},
        {"fieldname": "penalty_risk", "label": "Penalty Risk (₹)", "fieldtype": "Currency", "width": 130},
    ]


def get_data(filters):
    conditions = {}

    if filters:
        if filters.get("from_date"):
            conditions["due_date"] = [">=", filters.get("from_date")]
        if filters.get("to_date"):
            conditions["due_date"] = ["<=", filters.get("to_date")]
        if filters.get("compliance_type"):
            conditions["compliance_type"] = filters.get("compliance_type")
        if filters.get("status"):
            conditions["status"] = filters.get("status")
        if filters.get("assigned_to"):
            conditions["assigned_to"] = filters.get("assigned_to")

    tasks = frappe.get_all(
        "Compliance Task",
        filters=conditions,
        fields=[
            "name", "client_engagement", "task_name", "form_number",
            "compliance_type", "due_date", "status", "assigned_to", "penalty_risk",
        ],
        order_by="due_date asc",
    )

    data = []
    for task in tasks:
        days_overdue = 0
        if task.due_date and task.status not in ("Filed", "Waived"):
            diff = date_diff(today(), task.due_date)
            if diff > 0:
                days_overdue = diff

        # Get client name from engagement
        client = frappe.db.get_value(
            "Client Engagement", task.client_engagement, "client"
        ) if task.client_engagement else ""

        data.append({
            "client": client,
            "task_name": task.task_name,
            "form_number": task.form_number,
            "compliance_type": task.compliance_type,
            "due_date": task.due_date,
            "days_overdue": days_overdue,
            "status": task.status,
            "assigned_to": task.assigned_to,
            "penalty_risk": flt(task.penalty_risk),
        })

    return data


def get_chart(data):
    filed = sum(1 for d in data if d["status"] == "Filed")
    pending = sum(1 for d in data if d["status"] in ("Pending", "In Progress"))
    overdue = sum(1 for d in data if d["days_overdue"] > 0 and d["status"] != "Filed")

    return {
        "data": {
            "labels": ["Filed", "Pending", "Overdue"],
            "datasets": [{"values": [filed, pending, overdue]}],
        },
        "type": "donut",
        "colors": ["#28a745", "#ffc107", "#dc3545"],
    }
