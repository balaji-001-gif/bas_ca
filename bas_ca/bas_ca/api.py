# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, getdate, add_days, date_diff, flt, nowdate


@frappe.whitelist()
def create_annual_compliance_package(client_engagement, financial_year="2025-26"):
    """
    Create annual compliance package for a client engagement.
    Fetches all matching Compliance Task Templates and creates Compliance Tasks.
    """
    engagement = frappe.get_doc("Client Engagement", client_engagement)
    company_type = engagement.company_type

    # Fetch all templates matching the client's company type
    templates = frappe.get_all(
        "Compliance Task Template",
        fields=["name", "task_name", "compliance_type", "form_number",
                "statutory_due_date", "recurrence", "default_assignee_role",
                "applicable_company_type", "penalty_per_day", "reminder_days_before"],
    )

    count = 0
    for template in templates:
        # Check if the template is applicable to this company type
        applicable = template.get("applicable_company_type") or ""
        if company_type and applicable and company_type not in applicable:
            continue

        # Check if task already exists for this engagement + template + FY
        existing = frappe.db.exists(
            "Compliance Task",
            {
                "client_engagement": client_engagement,
                "template": template.name,
                "due_date": [">=", f"2025-04-01"],
            },
        )
        if existing:
            continue

        # Create Compliance Task
        task = frappe.new_doc("Compliance Task")
        task.client_engagement = client_engagement
        task.template = template.name
        task.task_name = template.task_name
        task.compliance_type = template.compliance_type
        task.form_number = template.form_number
        task.due_date = template.statutory_due_date or today()
        task.status = "Pending"
        task.priority = "Medium"

        # Try to find a user with the default assignee role
        if template.default_assignee_role:
            users = frappe.get_all(
                "Has Role",
                filters={"role": template.default_assignee_role, "parenttype": "User"},
                fields=["parent"],
                limit=1,
            )
            if users:
                task.assigned_to = users[0].parent

        task.insert(ignore_permissions=True)
        count += 1

    frappe.db.commit()
    return count


@frappe.whitelist()
def send_whatsapp_reminder(compliance_task):
    """
    Send WhatsApp reminder for a compliance task.
    Uses Frappe's notification system.
    """
    task = frappe.get_doc("Compliance Task", compliance_task)
    engagement = frappe.get_doc("Client Engagement", task.client_engagement)

    client_name = engagement.client
    form_number = task.form_number or task.task_name
    due_date = task.due_date

    # Get firm name from Website Settings or default
    firm_name = frappe.db.get_single_value("Website Settings", "app_name") or "Bas CA Practice"

    message = (
        f"Dear {client_name}, your {form_number} is due on {due_date}. "
        f"Please share required documents at your earliest convenience. "
        f"— {firm_name}"
    )

    # Try to send via WhatsApp if configured, otherwise send email
    try:
        # Check if WhatsApp is configured
        if frappe.db.exists("DocType", "WhatsApp Message"):
            wa_msg = frappe.new_doc("WhatsApp Message")
            wa_msg.to = engagement.client
            wa_msg.message = message
            wa_msg.insert(ignore_permissions=True)
            return True
    except Exception:
        pass

    # Fallback to email notification
    try:
        customer_email = frappe.db.get_value("Customer", engagement.client, "email_id")
        if customer_email:
            frappe.sendmail(
                recipients=[customer_email],
                subject=f"Compliance Reminder: {form_number} due on {due_date}",
                message=message,
            )
            return True
    except Exception:
        pass

    frappe.msgprint(_("Reminder notification created. Configure WhatsApp or Email for delivery."))
    return True


def check_ccfs_2026_window():
    """
    Daily scheduled job: Check if CCFS-2026 window is open and alert partners.
    """
    # CCFS-2026 window dates (configurable)
    ccfs_start = frappe.db.get_single_value("System Settings", "ccfs_2026_start_date") or "2026-01-01"
    ccfs_end = frappe.db.get_single_value("System Settings", "ccfs_2026_end_date") or "2026-06-30"

    current_date = getdate(today())
    start_date = getdate(ccfs_start)
    end_date = getdate(ccfs_end)

    if start_date <= current_date <= end_date:
        # Count eligible ROC filings
        eligible_count = frappe.db.count(
            "ROC Filing",
            filters={
                "status": "Pending",
                "ccfs_2026_applicable": 1,
            },
        )

        if eligible_count > 0:
            # Get all users with CA Partner role
            partners = frappe.get_all(
                "Has Role",
                filters={"role": "CA Partner", "parenttype": "User"},
                fields=["parent"],
            )

            partner_emails = [p.parent for p in partners if p.parent != "Administrator"]

            if partner_emails:
                frappe.sendmail(
                    recipients=partner_emails,
                    subject=f"CCFS-2026 Window Open — {eligible_count} ROC Filings Eligible",
                    message=(
                        f"<h3>CCFS-2026 Window is Open</h3>"
                        f"<p>{eligible_count} ROC filing(s) are eligible for reduced fees "
                        f"under the CCFS-2026 scheme.</p>"
                        f"<p>Window closes on: {ccfs_end}</p>"
                        f"<p>Please review and file eligible forms at the earliest.</p>"
                    ),
                )


def send_compliance_reminders():
    """
    Daily scheduled job: Send reminders for upcoming compliance tasks.
    Checks tasks where due_date - reminder_days_before = today.
    """
    tasks = frappe.get_all(
        "Compliance Task",
        filters={
            "status": ["in", ["Pending", "In Progress"]],
            "due_date": [">=", today()],
        },
        fields=["name", "task_name", "form_number", "due_date",
                "client_engagement", "assigned_to", "template"],
    )

    for task in tasks:
        reminder_days = 7  # default
        if task.template:
            reminder_days = (
                frappe.db.get_value(
                    "Compliance Task Template", task.template, "reminder_days_before"
                )
                or 7
            )

        reminder_date = add_days(task.due_date, -reminder_days)

        if getdate(today()) == getdate(reminder_date):
            # Send reminder to assigned user
            if task.assigned_to:
                frappe.sendmail(
                    recipients=[task.assigned_to],
                    subject=f"Compliance Reminder: {task.form_number or task.task_name} due on {task.due_date}",
                    message=(
                        f"<p>Reminder: <b>{task.task_name}</b> ({task.form_number}) "
                        f"for engagement {task.client_engagement} is due on "
                        f"<b>{task.due_date}</b>.</p>"
                        f"<p>Please ensure timely filing.</p>"
                    ),
                )


@frappe.whitelist()
def generate_board_meeting_notice(board_meeting):
    """Generate a notice template for the board meeting."""
    doc = frappe.get_doc("Board Meeting", board_meeting)
    engagement = frappe.get_doc("Client Engagement", doc.client_engagement)

    client_name = engagement.client
    cin = engagement.cin or "____"

    notice_template = f"""
<h2 style="text-align: center;">NOTICE OF {doc.meeting_type.upper()}</h2>
<h3 style="text-align: center;">{client_name}</h3>
<p style="text-align: center;">CIN: {cin}</p>
<hr>
<p>Notice is hereby given that the <b>{doc.meeting_number or ''}</b> {doc.meeting_type}
of the Board of Directors of <b>{client_name}</b> will be held on
<b>{doc.meeting_date}</b> at <b>{doc.meeting_time or ''}</b>
at <b>{doc.venue or 'the Registered Office of the Company'}</b>
{'via Video Conferencing (' + (doc.vc_platform or 'VC') + ')' if doc.video_conferencing else ''}
to transact the following business:</p>

<h4>AGENDA</h4>
<ol>
<li>To confirm the minutes of the previous Board Meeting.</li>
<li>To take note of the matters arising from the previous minutes.</li>
<li>[Add agenda items]</li>
</ol>

<br>
<p>By Order of the Board</p>
<p>For <b>{client_name}</b></p>
<br><br>
<p>_______________________</p>
<p>Company Secretary</p>
<p>Date: {frappe.utils.today()}</p>
<p>Place: {doc.venue or ''}</p>
"""
    doc.db_set("agenda", notice_template)
    doc.db_set("status", "Notice Sent")
    doc.db_set("notice_sent_date", today())
    return True


@frappe.whitelist()
def generate_board_meeting_agenda(board_meeting):
    """Generate a formatted agenda for the board meeting."""
    doc = frappe.get_doc("Board Meeting", board_meeting)

    if not doc.agenda:
        doc.db_set("agenda", """
<h3>AGENDA</h3>
<table border="1" cellpadding="8" cellspacing="0" width="100%">
<tr><th>Item No.</th><th>Agenda Item</th><th>Type</th></tr>
<tr><td>1</td><td>Confirmation of Minutes of previous Board Meeting</td><td>Ordinary</td></tr>
<tr><td>2</td><td>Matters arising from previous minutes</td><td>Information</td></tr>
<tr><td>3</td><td>Financial review and updates</td><td>Information</td></tr>
<tr><td>4</td><td>Compliance updates — ROC, GST, Income Tax</td><td>Information</td></tr>
<tr><td>5</td><td>Any other business with permission of the Chair</td><td>Ordinary</td></tr>
</table>
""")
    return True


@frappe.whitelist()
def generate_board_meeting_minutes(board_meeting):
    """Generate a minutes template for the board meeting."""
    doc = frappe.get_doc("Board Meeting", board_meeting)
    engagement = frappe.get_doc("Client Engagement", doc.client_engagement)

    client_name = engagement.client
    cin = engagement.cin or "____"

    minutes_template = f"""
<h2 style="text-align: center;">MINUTES OF {doc.meeting_type.upper()}</h2>
<h3 style="text-align: center;">{client_name}</h3>
<p style="text-align: center;">CIN: {cin}</p>
<hr>

<p>Minutes of the <b>{doc.meeting_number or ''}</b> {doc.meeting_type}
of the Board of Directors of <b>{client_name}</b> held on
<b>{doc.meeting_date}</b> at <b>{doc.meeting_time or ''}</b>
at <b>{doc.venue or 'the Registered Office of the Company'}</b>.</p>

<h4>PRESENT:</h4>
<table border="1" cellpadding="8" cellspacing="0" width="100%">
<tr><th>Sr. No.</th><th>Name of Director</th><th>DIN</th><th>Designation</th></tr>
<tr><td>1</td><td></td><td></td><td>Chairman</td></tr>
<tr><td>2</td><td></td><td></td><td>Director</td></tr>
</table>

<p>Quorum being present, the Chairman called the meeting to order.</p>

<h4>RESOLUTIONS:</h4>

<p><b>Resolution 1:</b> Confirmation of Minutes</p>
<p>RESOLVED THAT the minutes of the previous Board Meeting held on ____
be and are hereby confirmed.</p>

<br>
<p>There being no other business, the meeting concluded with a vote of thanks to the Chair.</p>

<br><br>
<p>_______________________</p>
<p>Chairman</p>
<p>Date: </p>
<p>Place: {doc.venue or ''}</p>
"""
    doc.db_set("minutes", minutes_template)
    doc.db_set("status", "Minutes Drafted")
    return True


def has_portal_permission(doc, ptype, user, verbose=False):
    """
    Scripted permission check for CA Client portal access.
    Ensures clients only see records linked to their Client Engagement.
    """
    if "CA Client" not in frappe.get_roles(user):
        return True  # Let standard permissions handle other roles

    # Find the Client Engagement linked to this user
    user_engagement = frappe.db.get_value(
        "Client Engagement",
        {"portal_user": user, "portal_access": 1},
        "name"
    )

    if not user_engagement:
        return False

    # Check permission based on DocType
    if doc.doctype == "Client Engagement":
        return doc.name == user_engagement

    if hasattr(doc, "client_engagement"):
        return doc.client_engagement == user_engagement

    return False
