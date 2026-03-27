// Copyright (c) 2026, Antigravity and contributors
// For license information, please see license.txt

frappe.ui.form.on("GST Return Tracker", {
    refresh(frm) {
        // Show ITC mismatch warning
        if (frm.doc.itc_difference && Math.abs(frm.doc.itc_difference) > 1000) {
            frm.dashboard.set_headline_alert(
                '<div class="alert alert-warning">⚠️ ITC Mismatch: ₹' +
                    frm.doc.itc_difference.toLocaleString("en-IN") +
                    "</div>"
            );
        }
    },
    itc_as_per_2b(frm) {
        frm.set_value(
            "itc_difference",
            (frm.doc.itc_as_per_2b || 0) - (frm.doc.itc_claimed || 0)
        );
    },
    itc_claimed(frm) {
        frm.set_value(
            "itc_difference",
            (frm.doc.itc_as_per_2b || 0) - (frm.doc.itc_claimed || 0)
        );
    },
});
