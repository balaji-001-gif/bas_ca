import frappe
from frappe.utils import today, getdate

def get_context(context):
    """
    Premium CA Portal Controller v2.
    Streamlined, high-performance data fetching with robust error handling.
    """
    # 0. Performance & Security
    context.no_cache = 1
    user = frappe.session.user
    
    # 1. Provide safe base structure
    context.update({
        "client_name": "Portal",
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
        "tasks": [],
        "show_sidebar": True,
        "access_denied": False,
        "is_administrator": (user == "Administrator"),
        "debug_info": {"user": user, "engagement_found": False}
    })

    # Redirect Guests
    if user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/bas-ca-portal"
        raise frappe.Redirect

    try:
        # 2. Find Engagement
        engagement_data = frappe.db.get_value(
            "Client Engagement",
            {"portal_user": user},
            ["name", "client", "engagement_status", "portal_access"],
            as_dict=True
        )
        
        # Admin Fallback
        if not engagement_data and user == "Administrator":
            engagement_data = frappe.db.get_value(
                "Client Engagement",
                {"portal_access": 1},
                ["name", "client", "engagement_status", "portal_access"],
                as_dict=True
            )
            if engagement_data:
                frappe.msgprint("Diagnostic: Showing first active engagement for Administrator.")

        if not engagement_data:
            context.client_name = "Guest / Unlinked User"
            context.show_sidebar = False
            return context

        # 3. Access Control
        engagement_name = engagement_data.name
        context.debug_info.update({
            "engagement_found": True,
            "engagement_name": engagement_name,
            "portal_access": bool(engagement_data.portal_access)
        })

        if not engagement_data.portal_access:
            context.access_denied = True
            context.client_name = engagement_data.client or "Access Restricted"
            context.show_sidebar = False
            return context

        # 4. Data Aggregation (Single-Pass preferred but get_all is fast)
        all_tasks = frappe.get_all(
            "Compliance Task",
            filters={"client_engagement": engagement_name},
            fields=["name", "task_name", "status", "due_date", "form_number", "compliance_type", "assigned_to"],
            order_by="due_date asc"
        )
        
        # Metrics & Lists
        pending = [t for t in all_tasks if t.status in ["Pending", "In Progress", "Review"]]
        overdue = [t for t in all_tasks if t.due_date and getdate(t.due_date) < getdate(today()) and t.status not in ["Filed", "Waived"]]
        filed = [t for t in all_tasks if t.status == "Filed"]
        approvals = [t for t in all_tasks if t.status == "Review"]
        
        # Activity (Comments on the engagement)
        activity = frappe.get_all(
            "Comment",
            filters={"reference_doctype": "Client Engagement", "reference_name": engagement_name},
            fields=["content", "comment_by", "creation"],
            limit=10,
            order_by="creation desc"
        )
        
        # Logic for Next Deadline
        next_dl = "N/A"
        next_dl_task = ""
        upcoming = [t for t in all_tasks if t.due_date and t.status not in ["Filed", "Waived"]]
        if upcoming:
            # Already sorted by due_date asc in SQL query
            next_dl = upcoming[0].due_date
            next_dl_task = upcoming[0].task_name

        # Calculate Health Score
        score = 100
        if all_tasks:
            score = int((len(filed) / len(all_tasks)) * 100)

        # 5. Final Context Update
        context.update({
            "client_name": engagement_data.client or "Client",
            "engagement_name": engagement_name,
            "health_score": score,
            "pending_tasks_count": len(pending),
            "overdue_count": len(overdue),
            "filed_count": len(filed),
            "total_tasks": len(all_tasks),
            "tasks": all_tasks,
            "pending_approvals": approvals,
            "recent_activity": activity,
            "next_deadline": next_dl,
            "next_deadline_task": next_dl_task,
            "engagement_status": engagement_data.engagement_status or "Active"
        })

    except Exception as e:
        frappe.log_error(f"Portal v2 Controller Error: {str(e)}")
        context.system_error = str(e)
        context.client_name = "Portal (Error)"

    context.title = f"Command Center - {context.get('client_name', 'Portal')}"
    return context
