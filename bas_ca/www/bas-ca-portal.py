import frappe

def get_context(context):
    """
    Context for the CA Client Portal Dashboard.
    Uses standard Frappe login — no custom login needed.
    Always injects safe defaults so the template never throws UndefinedError.
    """
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/bas-ca-portal"
        raise frappe.Redirect

    # Safe defaults — template will NEVER get UndefinedError
    defaults = {
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
    context.update(defaults)

    try:
        get_data = frappe.get_attr("bas_ca.bas_ca.api.get_portal_full_data")
        data = get_data(frappe.session.user)
        context.update(data)
    except Exception as e:
        frappe.log_error(f"Portal Context Error: {str(e)}")

    context.show_sidebar = False
    context.no_breadcrumbs = True
    context.title = "Client Command Center"
