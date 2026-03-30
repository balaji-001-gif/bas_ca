app_name = "bas_ca"
app_title = "Bas CA"
app_publisher = "Antigravity"
app_description = "CA & CS Practice Management for Indian firms"
app_email = "dev@antigravity.in"
app_license = "MIT"
app_version = "1.0.0"

# Required Apps
# -------------
required_apps = ["erpnext"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bas_ca/css/bas_ca.css"
# app_include_js = "/assets/bas_ca/js/bas_ca.js"

# include js, css files in header of web template
# web_include_css = "/assets/bas_ca/css/bas_ca.css"
# web_include_js = "/assets/bas_ca/js/bas_ca.js"

# include custom scss in every website theme (without signing in)
# website_theme_scss = "bas_ca/public/scss/website"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Favicon
# -----------
# app_logo_url = "/assets/bas_ca/images/logo.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
role_home_page = {
	"CA Client": "bas-ca-portal"
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "bas_ca.utils.jinja_methods",
#	"filters": "bas_ca.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "bas_ca.install.before_install"
# after_install = "bas_ca.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bas_ca.uninstall.before_uninstall"
# after_uninstall = "bas_ca.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "bas_ca.utils.before_app_install"
# after_app_install = "bas_ca.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "bas_ca.utils.before_app_uninstall"
# after_app_uninstall = "bas_ca.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bas_ca.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

has_permission = {
    "Client Engagement": "bas_ca.bas_ca.api.has_portal_permission",
    "Compliance Task": "bas_ca.bas_ca.api.has_portal_permission",
    "GST Return Tracker": "bas_ca.bas_ca.api.has_portal_permission",
    "ROC Filing": "bas_ca.bas_ca.api.has_portal_permission",
}

portal_menu_items = [
    {"title": "Dashboard", "route": "/bas-ca-portal", "role": "CA Client", "icon": "fa fa-dashboard"},
    {"title": "My Engagement", "route": "/client-engagement", "role": "CA Client"},
    {"title": "Compliance Tasks", "route": "/compliance-tasks", "role": "CA Client"},
    {"title": "GST Returns", "route": "/gst-returns", "role": "CA Client"},
    {"title": "ROC Filings", "route": "/roc-filings", "role": "CA Client"},
]

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Compliance Task": {
        "validate": "bas_ca.bas_ca.doctype.compliance_task.compliance_task.calculate_penalty_risk",
    },
    "GST Return Tracker": {
        "validate": "bas_ca.bas_ca.doctype.gst_return_tracker.gst_return_tracker.calculate_itc_difference",
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "bas_ca.bas_ca.api.check_ccfs_2026_window",
        "bas_ca.bas_ca.api.send_compliance_reminders",
    ],
}

# Testing
# -------

# before_tests = "bas_ca.install.before_tests"

# Overriding Methods
# --------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "bas_ca.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the arguments of the original function
#
# overriding_methods = {
#	"frappe.desk.doctype.event.event.get_events": "bas_ca.event.get_events"
# }

# exempt linked doctypes from hierarchical permissions
# -----------------------------------------------------------
# exempt_doctypes_from_hierarchical_permissions = ["DocType"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"bas_ca.auth.validate"
# ]

# Fixtures
# --------
fixtures = [
    {
        "dt": "Workflow",
        "filters": [["name", "in", [
            "GST Return Workflow",
            "ROC Filing Workflow",
            "Compliance Task Workflow",
            "Board Meeting Workflow",
            "Secretarial Audit Workflow",
        ]]],
    },
    {
        "dt": "Workflow State",
        "filters": [["name", "in", [
            "Pending", "Data Prepared", "Under Review", "Approved", "Filed",
            "Archived", "Drafted", "Client Approval", "SRN Received",
            "In Progress", "Review Pending", "Scheduled", "Notice Sent",
            "Held", "Minutes Drafted", "Minutes Approved", "Initiated",
            "Draft Report", "Final Report", "Submitted",
        ]]],
    },
    {
        "dt": "Workflow Action Master",
        "filters": [["name", "in", [
            "Prepare Data", "Submit for Review", "Approve", "File",
            "Archive", "Draft", "Send for Client Approval", "Record SRN",
            "Start Work", "Submit for Review", "Mark as Filed",
            "Send Notice", "Mark as Held", "Draft Minutes",
            "Approve Minutes", "Start Audit", "Create Draft Report",
            "Finalize Report", "Submit Report",
        ]]],
    },
    {
        "dt": "Role",
        "filters": [["name", "in", [
            "CA Partner", "CA Manager", "CA Staff", "CS Executive", "CA Client",
        ]]],
    },
    {
        "dt": "Compliance Task Template",
    },
    {
        "dt": "Dashboard Chart",
        "filters": [["module", "=", "Bas Ca"]],
    },
    {
        "dt": "Number Card",
        "filters": [["module", "=", "Bas Ca"]],
    },
    {
        "dt": "Workflow State",
    },
    {
        "dt": "Workspace",
        "filters": [["name", "=", "Bas CA Practice Management"]],
    },
]
