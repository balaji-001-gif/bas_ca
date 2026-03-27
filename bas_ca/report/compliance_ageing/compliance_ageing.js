// Copyright (c) 2026, Antigravity and contributors
// For license information, please see license.txt

frappe.query_reports["Compliance Ageing"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -12),
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
        },
        {
            fieldname: "compliance_type",
            label: __("Compliance Type"),
            fieldtype: "Select",
            options: "\nGST\nIncome Tax\nTDS\nROC\nSecretarial\nAudit",
        },
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: "\nPending\nIn Progress\nReview\nFiled\nOverdue\nWaived",
        },
        {
            fieldname: "assigned_to",
            label: __("Assigned To"),
            fieldtype: "Link",
            options: "User",
        },
    ],
};
