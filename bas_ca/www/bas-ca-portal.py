import frappe
from frappe.utils import today, getdate

def get_context(context):
    """
    Context for the CA Client Portal Dashboard.
    Uses standard Frappe login — no custom login needed.
    """
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/bas-ca-portal"
        raise frappe.Redirect

    try:
        get_portal_full_data = frappe.get_attr("bas_ca.bas_ca.api.get_portal_full_data")
        data = get_portal_full_data(frappe.session.user)
    except Exception as e:
        frappe.log_error(f"Portal Context Error: {str(e)}")
        data = {
            "client_name": "Client Portal",
            "engagement_name": None,
            "health_score": 0,
            "pending_tasks_count": 0,
            "overdue_count": 0,
            "filed_count": 0,
            "total_tasks": 0,
            "next_deadline": "N/A",
            "next_deadline_task": "",
            "engagement_status": "Active",
            "recent_activity": [],
            "pending_approvals": [],
            "tasks": []
        }

    context.update(data)
    context.show_sidebar = False
    context.no_breadcrumbs = True
    context.title = "Client Command Center"
