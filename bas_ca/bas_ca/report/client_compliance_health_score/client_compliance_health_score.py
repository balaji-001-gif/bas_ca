# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, getdate, flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {"fieldname": "client", "label": "Client", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"fieldname": "filing_score", "label": "Filing Score (20)", "fieldtype": "Int", "width": 120},
        {"fieldname": "itc_score", "label": "ITC Score (20)", "fieldtype": "Int", "width": 110},
        {"fieldname": "roc_score", "label": "ROC Score (20)", "fieldtype": "Int", "width": 110},
        {"fieldname": "meeting_score", "label": "Meeting Score (20)", "fieldtype": "Int", "width": 130},
        {"fieldname": "kyc_score", "label": "KYC Score (20)", "fieldtype": "Int", "width": 110},
        {"fieldname": "total_score", "label": "Total Score (100)", "fieldtype": "Int", "width": 120},
        {"fieldname": "health", "label": "Health", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    engagements = frappe.get_all(
        "Client Engagement",
        filters={"engagement_status": "Active"},
        fields=["name", "client", "company_type"],
    )

    data = []
    for eng in engagements:
        scores = calculate_health_score(eng.name, eng.company_type)
        total = sum(scores.values())

        if total >= 80:
            health = "🟢 Green"
        elif total >= 50:
            health = "🟡 Amber"
        else:
            health = "🔴 Red"

        data.append({
            "client": eng.client,
            "filing_score": scores["filing"],
            "itc_score": scores["itc"],
            "roc_score": scores["roc"],
            "meeting_score": scores["meeting"],
            "kyc_score": scores["kyc"],
            "total_score": total,
            "health": health,
        })

    data.sort(key=lambda x: x["total_score"], reverse=True)
    return data


def calculate_health_score(engagement, company_type):
    """Calculate 0-100 health score across 5 dimensions (20 pts each)."""
    scores = {
        "filing": 0,
        "itc": 0,
        "roc": 0,
        "meeting": 0,
        "kyc": 0,
    }

    # 1. Filing Score (20 pts): All tasks filed on time this FY
    total_tasks = frappe.db.count("Compliance Task", {"client_engagement": engagement})
    filed_tasks = frappe.db.count(
        "Compliance Task",
        {"client_engagement": engagement, "status": "Filed"},
    )
    overdue_tasks = frappe.db.count(
        "Compliance Task",
        {
            "client_engagement": engagement,
            "status": ["not in", ["Filed", "Waived"]],
            "due_date": ["<", today()],
        },
    )
    if total_tasks > 0:
        filing_ratio = filed_tasks / total_tasks
        scores["filing"] = int(filing_ratio * 20) - min(overdue_tasks * 2, 10)
        scores["filing"] = max(0, scores["filing"])
    else:
        scores["filing"] = 20  # No tasks = not applicable = full score

    # 2. ITC Score (20 pts): No ITC mismatches
    gst_returns = frappe.get_all(
        "GST Return Tracker",
        filters={"client_engagement": engagement},
        fields=["itc_difference"],
    )
    mismatch_count = sum(1 for g in gst_returns if abs(flt(g.itc_difference)) > 1000)
    if gst_returns:
        if mismatch_count == 0:
            scores["itc"] = 20
        else:
            scores["itc"] = max(0, 20 - (mismatch_count * 5))
    else:
        scores["itc"] = 20

    # 3. ROC Score (20 pts): All ROC filings up to date
    total_roc = frappe.db.count("ROC Filing", {"client_engagement": engagement})
    filed_roc = frappe.db.count(
        "ROC Filing",
        {"client_engagement": engagement, "status": ["in", ["Filed", "SRN Generated", "Approved"]]},
    )
    if total_roc > 0:
        scores["roc"] = int((filed_roc / total_roc) * 20)
    else:
        scores["roc"] = 20

    # 4. Meeting Score (20 pts): Board meetings held as per SS-1 (min 4 per FY)
    meetings_held = frappe.db.count(
        "Board Meeting",
        {
            "client_engagement": engagement,
            "status": ["in", ["Held", "Minutes Drafted", "Minutes Approved", "Filed"]],
        },
    )
    if company_type in ("Private Limited", "OPC", "Startup"):
        required_meetings = 4
        scores["meeting"] = min(int((meetings_held / required_meetings) * 20), 20)
    else:
        scores["meeting"] = 20  # Not required for LLP/Partnership/Proprietorship

    # 5. KYC Score (20 pts): DSC/KYC up to date
    # Check DIR-3 KYC filing
    kyc_filed = frappe.db.count(
        "Compliance Task",
        {
            "client_engagement": engagement,
            "form_number": ["like", "%DIR-3%"],
            "status": "Filed",
        },
    )
    kyc_total = frappe.db.count(
        "Compliance Task",
        {
            "client_engagement": engagement,
            "form_number": ["like", "%DIR-3%"],
        },
    )
    if kyc_total > 0:
        scores["kyc"] = int((kyc_filed / kyc_total) * 20)
    else:
        scores["kyc"] = 20

    return scores


def get_chart(data):
    labels = [d["client"][:20] for d in data[:10]]
    values = [d["total_score"] for d in data[:10]]

    return {
        "data": {
            "labels": labels,
            "datasets": [{"name": "Health Score", "values": values}],
        },
        "type": "bar",
        "colors": ["#28a745"],
    }
