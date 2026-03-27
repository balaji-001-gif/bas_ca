# Bas CA — Frappe CA/CS Practice Management Module

A comprehensive CA & CS Practice Management Module built on Frappe/ERPNext v15+ for Indian accounting and company secretarial firms.

## 🚀 Features

### Core Modules (9 DocTypes)
| Module | Description |
|--------|------------|
| **Client Engagement** | Client onboarding with PAN, GSTIN, CIN, engagement type, fee structure |
| **Compliance Task Template** | 29+ pre-configured templates for GST, Income Tax, TDS, ROC |
| **Compliance Task** | Auto-generated tasks with penalty risk calculation |
| **GST Return Tracker** | ITC reconciliation with 2B mismatch detection |
| **ROC Filing** | CCFS-2026 support, MCA V3 ready |
| **Board Meeting** | Agenda, Minutes, Notice generation (SS-1/SS-2 compliant) |
| **Secretarial Audit** | Form MR-3 with 100+ checklist items |
| **Statutory Register** | Digital register management |
| **Time Log CA** | Effort tracking with billable hours |

### Automation
- ⚡ **Auto Compliance Package** — One-click annual compliance task creation
- 📊 **Penalty Risk Calculator** — Auto-calculates overdue penalties
- 🔍 **ITC Mismatch Detection** — Flags GST ITC differences > ₹1,000
- 📅 **CCFS-2026 Window Alert** — Daily email alerts for eligible ROC filings
- 📱 **WhatsApp/Email Reminders** — Automated filing reminders

### Reports (5 Script Reports)
1. **Compliance Ageing** — Color-coded overdue tracking with donut chart
2. **GST/TDS Reconciliation** — ITC mismatch flagging
3. **Penalty Avoidance** — Penalty saved by timely filing
4. **Revenue vs Effort** — Revenue per hour analysis
5. **Client Compliance Health Score** — 0-100 scoring across 5 dimensions

### Workflows (5 Document Workflows)
- GST Return Workflow (Pending → Filed → Archived)
- ROC Filing Workflow (Pending → Filed → SRN Received)
- Compliance Task Workflow (Pending → Filed)
- Board Meeting Workflow (Scheduled → Filed)
- Secretarial Audit Workflow (Initiated → Submitted)

### Print Formats (4 Jinja Templates)
- Board Meeting Notice
- Board Meeting Minutes (SS-1/SS-2 compliant)
- Engagement Letter
- Compliance Status Report (client-facing one-pager)

### Roles
| Role | Access |
|------|--------|
| CA Partner | Full access all doctypes |
| CA Manager | Read/write all, no delete |
| CA Staff | Read/write own assignments |
| CS Executive | ROC, Board Meeting, Secretarial Audit |
| CA Client | Portal read-only access |

## 📦 Installation

```bash
bench get-app https://github.com/balaji-001-gif/bas_ca.git
bench --site your-site install-app bas_ca
bench --site your-site migrate
```

## 📋 Requirements

- Frappe Framework v15+
- ERPNext v15+ (recommended)
- Python 3.10+
- MariaDB 10.6+ / PostgreSQL 14+

## 🇮🇳 India 2026 Ready

- ✅ MCA V3 form compatibility
- ✅ CCFS-2026 scheme support
- ✅ New GST portal logic
- ✅ Updated Income Tax due dates
- ✅ SS-1/SS-2 Secretarial Standards compliance
- ✅ 29+ pre-loaded compliance templates for FY 2025-26

## 📝 License

MIT — see [LICENSE](LICENSE)

## 👨‍💻 Publisher

**Antigravity** — dev@antigravity.in
