// Copyright (c) 2026, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on("ROC Filing", {
    refresh(frm) {
        if (frm.doc.ccfs_2026_applicable) {
            frm.dashboard.set_headline_alert(
                '<div class="alert alert-info">CCFS-2026 applicable — eligible for reduced fees</div>'
            );
        }
    },
});
