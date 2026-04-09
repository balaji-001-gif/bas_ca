import frappe
from frappe.utils import today, getdate

def get_context(context):
    """
    Context for the CA Client Portal Dashboard.
    All data fetching is inline — no api.py import needed.
    This works without bench restart since www/ .py files are loaded fresh.
    """
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/bas-ca-portal"
        raise frappe.Redirect

    # CRITICAL: Disable page caching so each user gets their own fresh data
    context.no_cache = 1

    # Always inject safe defaults first
    context.update({
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
    })

    try:
        user = frappe.session.user

        # Find Client Engagement linked to this user
        engagement_name = frappe.db.get_value(
            "Client Engagement",
            {"portal_user": user, "portal_access": 1},
            "name"
        )

        # Fallback for Administrator testing
        if not engagement_name and user == "Administrator":
            engagement_name = frappe.db.get_value("Client Engagement", {"portal_access": 1}, "name")
            if engagement_name:
                frappe.msgprint("Note: Showing first active engagement for Administrator testing.")

        if not engagement_name:
            context.client_name = "Guest / Unlinked User"
            context.engagement_status = "No Active"
            context.show_sidebar = False
            context.no_breadcrumbs = True
            context.title = "Client Command Center"
            frappe.msgprint("Your account is not yet linked to a Client Engagement. Please contact your CA.")
            return

        engagement = frappe.get_doc("Client Engagement", engagement_name)

        # Pending Tasks
        pending_tasks = frappe.get_all(
            "Compliance Task",
            filters={"client_engagement": engagement_name,
                     "status": ["not in", ["Filed", "Waived"]]},
            fields=["name", "task_name", "due_date", "status",
                    "compliance_type", "form_number", "assigned_to"]
        )

        # Overdue
        overdue_tasks = [
            t for t in pending_tasks
            if t.due_date and getdate(t.due_date) < getdate(today())
        ]

        # Filed count
        filed_count = frappe.db.count(
            "Compliance Task",
            {"client_engagement": engagement_name, "status": "Filed"}
        )
        total_tasks = frappe.db.count(
            "Compliance Task",
            {"client_engagement": engagement_name}
        )
        health_score = int((filed_count / total_tasks * 100)) if total_tasks > 0 else 100

        # Next Deadline
        next_task = frappe.get_all(
            "Compliance Task",
            filters={
                "client_engagement": engagement_name,
                "status": ["not in", ["Filed", "Waived"]],
                "due_date": [">=", today()]
            },
            fields=["due_date", "task_name"],
            order_by="due_date asc",
            limit=1
        )
        next_deadline = str(next_task[0].due_date) if next_task else "N/A"
        next_deadline_task = next_task[0].task_name if next_task else ""

        # All tasks ordered by due date
        all_tasks = frappe.get_all(
            "Compliance Task",
            filters={"client_engagement": engagement_name},
            fields=["name", "task_name", "due_date", "status",
                    "compliance_type", "form_number", "assigned_to"],
            order_by="due_date asc",
            limit=20
        )

        # Pending Approvals - Use 'Review' instead of non-existent 'Pending Client Approval'
        pending_approvals = frappe.get_all(
            "Compliance Task",
            filters={"client_engagement": engagement_name,
                     "status": "Review"},
            fields=["name", "task_name", "form_number", "due_date", "compliance_type"]
        )

        # Recent Activity (comments)
        try:
            activity = frappe.get_all(
                "Comment",
                filters={
                    "reference_doctype": "Client Engagement",
                    "reference_name": engagement_name
                },
                fields=["content", "creation", "comment_by", "comment_type"],
                order_by="creation desc",
                limit=8
            )
        except Exception:
            activity = []

        context.update({
            "client_name": engagement.client,
            "engagement_name": engagement_name,
            "health_score": health_score,
            "pending_tasks_count": len(pending_tasks),
            "overdue_count": len(overdue_tasks),
            "filed_count": filed_count,
            "total_tasks": total_tasks,
            "next_deadline": next_deadline,
            "next_deadline_task": next_deadline_task,
            "engagement_status": engagement.engagement_status or "Active",
            "recent_activity": activity,
            "pending_approvals": pending_approvals,
            "tasks": all_tasks
        })

    except Exception as e:
        frappe.log_error(f"Portal Context Error: {str(e)}")

    context.show_sidebar = False
    context.no_breadcrumbs = True
    context.title = "Client Command Center"
