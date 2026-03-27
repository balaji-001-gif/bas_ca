// Copyright (c) 2026, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on("Board Meeting", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("Generate Notice"), function () {
                frappe.call({
                    method: "bas_ca.bas_ca.api.generate_board_meeting_notice",
                    args: { board_meeting: frm.doc.name },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__("Board Meeting Notice generated"));
                            frm.reload_doc();
                        }
                    },
                });
            }, __("Generate"));

            frm.add_custom_button(__("Generate Agenda"), function () {
                frappe.call({
                    method: "bas_ca.bas_ca.api.generate_board_meeting_agenda",
                    args: { board_meeting: frm.doc.name },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__("Agenda generated and updated"));
                            frm.reload_doc();
                        }
                    },
                });
            }, __("Generate"));

            frm.add_custom_button(__("Generate Minutes"), function () {
                frappe.call({
                    method: "bas_ca.bas_ca.api.generate_board_meeting_minutes",
                    args: { board_meeting: frm.doc.name },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__("Minutes template generated"));
                            frm.reload_doc();
                        }
                    },
                });
            }, __("Generate"));
        }
    },
});
