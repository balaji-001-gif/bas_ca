import frappe

def get_context(context):
    """
    Context for the Bas CA Client Portal Dashboard.
    Ensures real-time compliance data is loaded via a resilient import.
    """
    if frappe.session.user == "Guest":
        frappe.throw("Please login to access the portal", frappe.PermissionError)

    # Use get_attr to be path-resilient
    try:
        get_portal_dashboard_data = frappe.get_attr("bas_ca.bas_ca.api.get_portal_dashboard_data")
        data = get_portal_dashboard_data(frappe.session.user)
    except Exception as e:
        frappe.log_error(f"Portal Data Error: {str(e)}")
        data = {
            "client_name": "Valued Client",
            "health_score": 0,
            "recent_filings": []
        }
        
    context.update(data)
    context.show_sidebar = True
    context.title = "Client Command Center"
