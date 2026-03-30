import frappe
from bas_ca.bas_ca.api import get_portal_dashboard_data

def get_context(context):
    """
    Context for the Bas CA Client Portal Dashboard.
    Fetches real-time compliance data for the logged-in client.
    """
    if frappe.session.user == "Guest":
        frappe.throw("Please login to access the portal", frappe.PermissionError)

    data = get_portal_dashboard_data(frappe.session.user)
    context.update(data)
    
    context.show_sidebar = True
    context.title = "Client Command Center"
