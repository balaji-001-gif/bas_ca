// Copyright (c) 2026, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on("Compliance Task", {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.status !== "Filed") {
            frm.add_custom_button(__("Send WhatsApp Reminder"), function () {
                frappe.call({
                    method: "bas_ca.bas_ca.api.send_whatsapp_reminder",
                    args: {
                        compliance_task: frm.doc.name,
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__("WhatsApp reminder sent successfully"));
                        }
                    },
                });
            }, __("Actions"));
        }

        // Color-code status indicator
        if (frm.doc.status === "Overdue") {
            frm.dashboard.set_headline_alert(
                '<div class="alert alert-danger">This task is overdue!</div>'
            );
        } else if (frm.doc.penalty_risk > 0) {
            frm.dashboard.set_headline_alert(
                '<div class="alert alert-warning">Penalty Risk: ₹' +
                    frm.doc.penalty_risk +
                    "</div>"
            );
        }
    },

    template(frm) {
        if (frm.doc.template) {
            frappe.db.get_doc("Compliance Task Template", frm.doc.template).then((doc) => {
                frm.set_value("task_name", doc.task_name);
                frm.set_value("compliance_type", doc.compliance_type);
                frm.set_value("form_number", doc.form_number);
                if (doc.statutory_due_date) {
                    frm.set_value("due_date", doc.statutory_due_date);
                }
            });
        }
    },
});
