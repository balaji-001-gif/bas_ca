// Copyright (c) 2026, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on("Client Engagement", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("Create Annual Compliance Package"), function () {
                let d = new frappe.ui.Dialog({
                    title: __("Create Annual Compliance Package"),
                    fields: [
                        {
                            label: "Financial Year",
                            fieldname: "financial_year",
                            fieldtype: "Data",
                            reqd: 1,
                            default: "2025-26",
                        },
                    ],
                    primary_action_label: __("Create"),
                    primary_action(values) {
                        frappe.call({
                            method: "bas_ca.api.create_annual_compliance_package",
                            args: {
                                client_engagement: frm.doc.name,
                                financial_year: values.financial_year,
                            },
                            callback: function (r) {
                                if (r.message) {
                                    frappe.msgprint(
                                        __("{0} compliance tasks created for FY {1}", [
                                            r.message,
                                            values.financial_year,
                                        ])
                                    );
                                    frm.reload_doc();
                                }
                            },
                        });
                        d.hide();
                    },
                });
                d.show();
            }, __("Actions"));
        }
    },
});
