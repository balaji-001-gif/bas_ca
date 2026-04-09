import frappe
from frappe import _

def get_context(context):
    """
    Context for the Bas CA Custom Login Page.
    Redirects if user is already logged in as a CA Client.
    """
    if frappe.session.user != "Guest":
        # Check if user has CA Client role
        if "CA Client" in frappe.get_roles(frappe.session.user):
            frappe.local.flags.redirect_location = "/bas-ca-portal"
            raise frappe.Redirect
            
    context.title = _("Financial Vanguard Portal Login")
    context.show_sidebar = False
    context.show_navbar = False
    context.show_footer = False
