# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {"fieldname": "client", "label": "Client", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"fieldname": "retainer_fee", "label": "Retainer Fee (₹)", "fieldtype": "Currency", "width": 140},
        {"fieldname": "total_invoiced", "label": "Total Invoiced (₹)", "fieldtype": "Currency", "width": 140},
        {"fieldname": "total_hours", "label": "Total Hours", "fieldtype": "Float", "width": 100},
        {"fieldname": "billable_hours", "label": "Billable Hours", "fieldtype": "Float", "width": 110},
        {"fieldname": "revenue_per_hour", "label": "Revenue/Hour (₹)", "fieldtype": "Currency", "width": 130},
    ]


def get_data(filters):
    engagements = frappe.get_all(
        "Client Engagement",
        filters={"engagement_status": "Active"},
        fields=["name", "client", "retainer_fee"],
    )

    data = []
    for eng in engagements:
        # Get total hours from Time Log CA
        time_logs = frappe.get_all(
            "Time Log CA",
            filters={"compliance_task": ["in",
                frappe.get_all("Compliance Task",
                    filters={"client_engagement": eng.name},
                    pluck="name") or ["__none__"]
            ]},
            fields=["sum(hours) as total_hours",
                     "sum(case when billable=1 then hours else 0 end) as billable_hours"],
        )

        total_hours = flt(time_logs[0].total_hours) if time_logs else 0
        billable_hours = flt(time_logs[0].billable_hours) if time_logs else 0

        # Get total invoiced (from Sales Invoice if ERPNext is installed)
        total_invoiced = flt(eng.retainer_fee)
        try:
            invoiced = frappe.db.sql(
                """SELECT SUM(grand_total) as total FROM `tabSales Invoice`
                WHERE customer = %s AND docstatus = 1""",
                eng.client, as_dict=True
            )
            if invoiced and invoiced[0].total:
                total_invoiced = flt(invoiced[0].total)
        except Exception:
            pass

        revenue_per_hour = flt(total_invoiced / billable_hours, 2) if billable_hours > 0 else 0

        data.append({
            "client": eng.client,
            "retainer_fee": flt(eng.retainer_fee),
            "total_invoiced": total_invoiced,
            "total_hours": total_hours,
            "billable_hours": billable_hours,
            "revenue_per_hour": revenue_per_hour,
        })

    # Sort by revenue_per_hour descending
    data.sort(key=lambda x: x["revenue_per_hour"], reverse=True)
    return data


def get_chart(data):
    labels = [d["client"] for d in data[:10]]
    values = [d["revenue_per_hour"] for d in data[:10]]

    return {
        "data": {
            "labels": labels,
            "datasets": [{"name": "Revenue per Hour", "values": values}],
        },
        "type": "bar",
    }
