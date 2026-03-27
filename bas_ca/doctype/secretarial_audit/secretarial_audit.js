// Copyright (c) 2026, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on("Secretarial Audit", {
    refresh(frm) {
        if (frm.doc.checklist_score >= 80) {
            frm.dashboard.set_headline_alert(
                '<div class="alert alert-success">Compliance Score: ' +
                    frm.doc.checklist_score + '%</div>'
            );
        } else if (frm.doc.checklist_score >= 50) {
            frm.dashboard.set_headline_alert(
                '<div class="alert alert-warning">Compliance Score: ' +
                    frm.doc.checklist_score + '%</div>'
            );
        } else if (frm.doc.checklist_score > 0) {
            frm.dashboard.set_headline_alert(
                '<div class="alert alert-danger">Compliance Score: ' +
                    frm.doc.checklist_score + '%</div>'
            );
        }
    },
});
