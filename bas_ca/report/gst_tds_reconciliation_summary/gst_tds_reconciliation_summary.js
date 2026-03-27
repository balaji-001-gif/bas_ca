// Copyright (c) 2026, Antigravity and contributors
frappe.query_reports["GST TDS Reconciliation Summary"] = {
    filters: [
        {
            fieldname: "financial_year",
            label: __("Financial Year"),
            fieldtype: "Data",
            default: "2025-26",
        },
        {
            fieldname: "return_type",
            label: __("Return Type"),
            fieldtype: "Select",
            options: "\nGSTR-1\nGSTR-3B\nGSTR-9\nGSTR-9C\nGSTR-4\nCMP-08",
        },
        {
            fieldname: "client_engagement",
            label: __("Client Engagement"),
            fieldtype: "Link",
            options: "Client Engagement",
        },
    ],
};
