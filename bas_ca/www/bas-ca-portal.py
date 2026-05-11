import frappe
from frappe.utils import today, getdate

def get_context(context):
    """
    Premium CA Portal Controller v3.
    Uses centralized API for data fetching to ensure consistency.
    """
    context.no_cache = 1
    user = frappe.session.user
    
    # Redirect Guests
    if user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/bas-ca-portal"
        raise frappe.Redirect

    try:
        from bas_ca.bas_ca.api import get_portal_full_data
        data = get_portal_full_data()
        
        if data.get("access_denied"):
            context.access_denied = True
            context.error_type = data.get("error_type")
            context.client_name = data.get("client_name") or "Access Restricted"
            context.show_sidebar = False
            context.title = "Access Restricted - Portal"
            return context

        context.update(data)
        context.show_sidebar = True
        context.debug_info = {
            "user": user,
            "engagement_found": True,
            "portal_access": True
        }
        context.title = f"Command Center - {context.get('client_name', 'Portal')}"

    except Exception as e:
        frappe.log_error(f"Portal v3 Controller Error: {str(e)}")
        context.system_error = str(e)
        context.client_name = "Portal (Error)"
        context.show_sidebar = False

    return context
    return context
