import frappe
from frappe.utils import today, getdate

def get_context(context):
    """
    Context for the CA Client Portal Dashboard.
    All data fetching is inline — no api.py import needed.
    This works without bench restart since www/ .py files are loaded fresh.
    """
    user = frappe.session.user
    
    # 1. Security: Don't allow Guest
    if user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/bas-ca-portal"
        raise frappe.Redirect
    
    # 2. Add defaults to context
    context.update({
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
        # 3. Find the client's active engagement (mapped to bas_ca)
        engagement = frappe.db.get_value(
            "Client Engagement",
            {"portal_user": user},  # portal_user is the correct field in bas_ca
            ["name", "client", "engagement_status", "portal_access"],
            as_dict=True
        )
        
        # Administrator fallback for testing
        if not engagement and user == "Administrator":
            engagement = frappe.db.get_value(
                "Client Engagement",
                {"portal_access": 1},
                ["name", "client", "engagement_status", "portal_access"],
                as_dict=True
            )
            if engagement:
                frappe.msgprint("Note: Showing first active engagement for Administrator testing.")

        if not engagement:
            context.access_denied = False
            context.client_name = "Guest / Unlinked User"
            context.debug_info = {"user": user, "engagement_found": False}
            context.show_sidebar = False
            return context
        
        engagement_name = engagement.name
        portal_access_on = bool(engagement.portal_access)

        if not portal_access_on:
            context.access_denied = True
            context.client_name = "Access Pending"
            context.debug_info = {"user": user, "engagement_found": True, "portal_access_on": False}
            context.show_sidebar = False
            return context

        # 4. Fetch all compliance tasks for this engagement
        tasks = frappe.get_all(
            "Compliance Task",
            filters={"client_engagement": engagement_name},
            fields=["name", "task_name", "status", "due_date", "form_number", "compliance_type", "assigned_to"],
            order_by="due_date asc"
        )
        
        # 5. Calculate metrics
        pending_tasks = [t for t in tasks if t.status in ["Pending", "In Progress", "Review"]]
        overdue_tasks = [
            t for t in tasks 
            if t.due_date and getdate(t.due_date) < getdate(today()) 
            and t.status not in ["Filed", "Waived"]
        ]
        filed_tasks = [t for t in tasks if t.status == "Filed"]
        
        # Pending approvals (Review status)
        pending_approvals = [t for t in tasks if t.status == "Review"]
        
        # Recent activity (comments on the engagement/tasks)
        recent_activity = frappe.get_all(
            "Comment",
            filters={
                "reference_doctype": "Client Engagement",
                "reference_name": engagement_name
            },
            fields=["content", "comment_by", "creation"],
            limit=8,
            order_by="creation desc"
        )
        
        # Next deadline
        next_deadline = "N/A"
        next_deadline_task = ""
        upcoming = [t for t in tasks if t.due_date and t.status not in ["Filed", "Waived"]]
        if upcoming:
            upcoming.sort(key=lambda x: getdate(x.due_date))
            next_deadline = str(upcoming[0].due_date)
            next_deadline_task = upcoming[0].task_name

        # Simple health score
        health_score = int((len(filed_tasks) / len(tasks) * 100)) if tasks else 100
        
        # 6. Pass everything to the template
        context.update({
            "client_name": engagement.client or "Client",
            "engagement_name": engagement_name,
            "health_score": health_score,
            "pending_tasks_count": len(pending_tasks),
            "overdue_count": len(overdue_tasks),
            "filed_count": len(filed_tasks),
            "total_tasks": len(tasks),
            "tasks": tasks,
            "pending_approvals": pending_approvals,
            "recent_activity": recent_activity,
            "next_deadline": next_deadline,
            "next_deadline_task": next_deadline_task,
            "engagement_status": engagement.engagement_status or "Active",
            "debug_info": {
                "user": user,
                "engagement_found": True,
                "portal_access_on": portal_access_on,
                "roles": frappe.get_roles(user)
            }
        })
        
        context.no_cache = 1
        
    except Exception as e:
        frappe.log_error(f"Portal Context Error: {str(e)}")
        context.error = str(e)

    context.show_sidebar = True
    context.no_breadcrumbs = True
    context.title = "Client Command Center"
    return context
