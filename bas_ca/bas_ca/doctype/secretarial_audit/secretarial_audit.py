# Copyright (c) 2026, Antigravity and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


DEFAULT_CHECKLIST_ITEMS = [
    # MOA/AOA
    {"area": "MOA/AOA", "check_item": "MOA/AOA obtained and reviewed"},
    {"area": "MOA/AOA", "check_item": "Objects clause reviewed for authorized activities"},
    {"area": "MOA/AOA", "check_item": "Authorized share capital verified with ROC records"},
    {"area": "MOA/AOA", "check_item": "Alteration of MOA (if any) filed with ROC within time"},
    {"area": "MOA/AOA", "check_item": "Special resolution for MOA alteration passed"},
    {"area": "MOA/AOA", "check_item": "AOA amendments properly filed (MGT-14)"},
    {"area": "MOA/AOA", "check_item": "Model AOA adoption verified (Table F/H/I/J)"},
    # Incorporation & Registered Office
    {"area": "Incorporation", "check_item": "Certificate of Incorporation obtained"},
    {"area": "Incorporation", "check_item": "Commencement of business certificate (INC-20A) filed"},
    {"area": "Incorporation", "check_item": "Registered office address verification (INC-22)"},
    {"area": "Incorporation", "check_item": "Change of registered office (if any) complied with Sec 12"},
    {"area": "Incorporation", "check_item": "Display of name and address at registered office"},
    # Board Meetings (SS-1)
    {"area": "Board Meetings", "check_item": "Minimum 4 board meetings held in FY (Sec 173)"},
    {"area": "Board Meetings", "check_item": "Gap between two board meetings not > 120 days"},
    {"area": "Board Meetings", "check_item": "Notice of BM given 7 days in advance"},
    {"area": "Board Meetings", "check_item": "Agenda circulated with notice"},
    {"area": "Board Meetings", "check_item": "Quorum present at all meetings (Sec 174)"},
    {"area": "Board Meetings", "check_item": "Minutes drafted within 30 days of meeting"},
    {"area": "Board Meetings", "check_item": "Minutes signed by Chairman at next meeting"},
    {"area": "Board Meetings", "check_item": "Minutes pages serially numbered"},
    {"area": "Board Meetings", "check_item": "Minutes book maintained as per Sec 118"},
    {"area": "Board Meetings", "check_item": "SS-1 Secretarial Standard on BM complied"},
    {"area": "Board Meetings", "check_item": "Interested directors disclosed interest (Sec 184)"},
    {"area": "Board Meetings", "check_item": "Leave of absence recorded for absent directors"},
    {"area": "Board Meetings", "check_item": "Participation via video conferencing complied with rules"},
    # General Meetings (SS-2)
    {"area": "General Meetings", "check_item": "AGM held within prescribed time (Sec 96)"},
    {"area": "General Meetings", "check_item": "AGM held during business hours and on working day"},
    {"area": "General Meetings", "check_item": "AGM notice given 21 clear days in advance"},
    {"area": "General Meetings", "check_item": "Explanatory statement annexed to notice (Sec 102)"},
    {"area": "General Meetings", "check_item": "Quorum present at general meetings (Sec 103)"},
    {"area": "General Meetings", "check_item": "Poll demanded/conducted as per rules"},
    {"area": "General Meetings", "check_item": "Results of AGM filed with ROC (MGT-15)"},
    {"area": "General Meetings", "check_item": "SS-2 Secretarial Standard on GM complied"},
    {"area": "General Meetings", "check_item": "E-voting facility provided (if applicable)"},
    {"area": "General Meetings", "check_item": "Scrutinizer appointed for e-voting/poll"},
    {"area": "General Meetings", "check_item": "EGM convened as per Sec 100 (if any)"},
    {"area": "General Meetings", "check_item": "Postal ballot conducted as per rules (if any)"},
    # Directors
    {"area": "Directors", "check_item": "All directors have valid DIN"},
    {"area": "Directors", "check_item": "DIR-3 KYC filed by all directors by Sep 30"},
    {"area": "Directors", "check_item": "Appointment of directors filed (DIR-12) within 30 days"},
    {"area": "Directors", "check_item": "Resignation of directors filed (DIR-12) within 30 days"},
    {"area": "Directors", "check_item": "Woman director appointed (if applicable - Sec 149)"},
    {"area": "Directors", "check_item": "Independent directors appointed (if applicable)"},
    {"area": "Directors", "check_item": "Maximum number of directorships not exceeded (Sec 165)"},
    {"area": "Directors", "check_item": "First meeting of Board held within 30 days of incorporation"},
    {"area": "Directors", "check_item": "Disqualified directors under Sec 164 checked"},
    {"area": "Directors", "check_item": "Form MBP-1 disclosure received from all directors"},
    {"area": "Directors", "check_item": "DIR-8 declaration of non-disqualification received"},
    {"area": "Directors", "check_item": "Disclosure of interest (Sec 184) obtained"},
    {"area": "Directors", "check_item": "Rotation of directors complied (if applicable)"},
    {"area": "Directors", "check_item": "ID declaration of independence obtained (Sec 149(7))"},
    # Key Managerial Personnel
    {"area": "KMP", "check_item": "KMP appointed as required (Sec 203)"},
    {"area": "KMP", "check_item": "Whole-time KMP not holding office in more than one company"},
    {"area": "KMP", "check_item": "Remuneration of KMP approved by Board/Committee"},
    # Charges
    {"area": "Charges", "check_item": "Register of charges maintained (Sec 85)"},
    {"area": "Charges", "check_item": "Creation of charge filed (CHG-1) within 30 days"},
    {"area": "Charges", "check_item": "Modification of charge filed (CHG-1) within 30 days"},
    {"area": "Charges", "check_item": "Satisfaction of charge filed (CHG-4) within 30 days"},
    {"area": "Charges", "check_item": "Charge ID obtained from ROC"},
    {"area": "Charges", "check_item": "Copy of instrument creating charge kept at registered office"},
    # Share Capital
    {"area": "Share Capital", "check_item": "Allotment of shares filed (PAS-3) within 30 days"},
    {"area": "Share Capital", "check_item": "Transfer of shares recorded in register"},
    {"area": "Share Capital", "check_item": "Share certificates issued within 2 months of allotment"},
    {"area": "Share Capital", "check_item": "Return of allotment filed with ROC"},
    {"area": "Share Capital", "check_item": "Buyback of shares complied with Sec 68-70 (if any)"},
    {"area": "Share Capital", "check_item": "Reduction of capital complied with Sec 66 (if any)"},
    {"area": "Share Capital", "check_item": "Demat compliance verified (if applicable)"},
    {"area": "Share Capital", "check_item": "Register of Members (MGT-1) maintained"},
    {"area": "Share Capital", "check_item": "Significant Beneficial Owner (BEN-2) filed"},
    # Annual Filings
    {"area": "Annual Filings", "check_item": "Annual Return (MGT-7/MGT-7A) filed within 60 days of AGM"},
    {"area": "Annual Filings", "check_item": "Financial Statements (AOC-4) filed within 30 days of AGM"},
    {"area": "Annual Filings", "check_item": "Auditor appointment (ADT-1) filed within 15 days of AGM"},
    {"area": "Annual Filings", "check_item": "DIR-3 KYC filed for all directors (Sec 153)"},
    {"area": "Annual Filings", "check_item": "MSME Form I filed (half-yearly)"},
    {"area": "Annual Filings", "check_item": "DPT-3 Return of Deposits filed (30 June)"},
    {"area": "Annual Filings", "check_item": "Cost Audit Report filed (if applicable)"},
    {"area": "Annual Filings", "check_item": "Secretarial Audit Report (MR-3) attached to Board Report"},
    # Statutory Registers
    {"area": "Statutory Registers", "check_item": "Register of Members (MGT-1) up to date"},
    {"area": "Statutory Registers", "check_item": "Register of Directors & KMP maintained"},
    {"area": "Statutory Registers", "check_item": "Register of Charges maintained"},
    {"area": "Statutory Registers", "check_item": "Register of Contracts (MBP-4) maintained"},
    {"area": "Statutory Registers", "check_item": "Register of Loans & Investments maintained"},
    {"area": "Statutory Registers", "check_item": "Register of Significant Beneficial Owners (BEN-4)"},
    # Related Party Transactions
    {"area": "Related Party Transactions", "check_item": "RPT policy approved by Board"},
    {"area": "Related Party Transactions", "check_item": "Prior approval of Audit Committee obtained (Sec 177)"},
    {"area": "Related Party Transactions", "check_item": "Ordinary resolution for RPTs in ordinary course"},
    {"area": "Related Party Transactions", "check_item": "Special resolution for material RPTs (if listed)"},
    {"area": "Related Party Transactions", "check_item": "Form AOC-2 disclosure in Board Report"},
    {"area": "Related Party Transactions", "check_item": "Arm's length pricing maintained"},
    # CSR
    {"area": "CSR", "check_item": "CSR applicability assessed (Sec 135)"},
    {"area": "CSR", "check_item": "CSR Committee constituted (if applicable)"},
    {"area": "CSR", "check_item": "CSR Policy formulated and disclosed on website"},
    {"area": "CSR", "check_item": "2% of average net profit spent on CSR"},
    {"area": "CSR", "check_item": "CSR-2 form filed with ROC"},
    {"area": "CSR", "check_item": "Unspent CSR amount transferred within prescribed time"},
    # Audit
    {"area": "Audit", "check_item": "Statutory auditor appointed as per Sec 139"},
    {"area": "Audit", "check_item": "Auditor appointment filed (ADT-1) with ROC"},
    {"area": "Audit", "check_item": "Auditor's report reviewed and discussed at AGM"},
    {"area": "Audit", "check_item": "Internal auditor appointed (if applicable - Sec 138)"},
    {"area": "Audit", "check_item": "Cost auditor appointed (if applicable - Sec 148)"},
    {"area": "Audit", "check_item": "Secretarial auditor appointed (if applicable - Sec 204)"},
    {"area": "Audit", "check_item": "Auditor rotation complied (Sec 139(2))"},
    {"area": "Audit", "check_item": "Audit Committee constituted (if applicable)"},
    # FEMA
    {"area": "FEMA", "check_item": "FDI compliance verified under FEMA"},
    {"area": "FEMA", "check_item": "ECB compliances checked"},
    {"area": "FEMA", "check_item": "FC-GPR/FC-TRS filed within time (if applicable)"},
    {"area": "FEMA", "check_item": "Annual Return on Foreign Liabilities & Assets (FLA) filed"},
    {"area": "FEMA", "check_item": "Downstream investment compliances verified"},
    # SEBI (if listed)
    {"area": "SEBI", "check_item": "LODR compliance (if listed company)"},
    {"area": "SEBI", "check_item": "Corporate governance report filed quarterly (if listed)"},
    {"area": "SEBI", "check_item": "Shareholding pattern filed quarterly (if listed)"},
    {"area": "SEBI", "check_item": "SAST compliances verified (if applicable)"},
    {"area": "SEBI", "check_item": "Insider trading code implemented (if listed)"},
    # Deposits
    {"area": "Deposits", "check_item": "Compliance with Sec 73-76 for acceptance of deposits"},
    {"area": "Deposits", "check_item": "DPT-3 Return filed by 30 June"},
    {"area": "Deposits", "check_item": "Deposit trust deed executed (if applicable)"},
    {"area": "Deposits", "check_item": "Deposit repayment reserve maintained"},
    # Dividend
    {"area": "Dividend", "check_item": "Dividend declared from distributable profits only"},
    {"area": "Dividend", "check_item": "Interim dividend declared as per AOA authorization"},
    {"area": "Dividend", "check_item": "Dividend paid within 30 days of declaration"},
    {"area": "Dividend", "check_item": "Transfer to Investor Education Fund after 7 years"},
    # Loans & Investments
    {"area": "Loans & Investments", "check_item": "Sec 185 - Loan to Directors compliance"},
    {"area": "Loans & Investments", "check_item": "Sec 186 - Loans and Investments compliance"},
    {"area": "Loans & Investments", "check_item": "Board/SR approval obtained for loans"},
]


class SecretarialAudit(Document):
    def validate(self):
        self.calculate_checklist_score()

    def before_insert(self):
        """Pre-populate checklist items if empty."""
        if not self.audit_checklist:
            self.populate_default_checklist()

    def populate_default_checklist(self):
        """Add 100+ default checklist items."""
        for idx, item in enumerate(DEFAULT_CHECKLIST_ITEMS, 1):
            self.append("audit_checklist", {
                "sr_no": idx,
                "area": item["area"],
                "check_item": item["check_item"],
                "complied": "NA",
                "remarks": "",
            })

    def calculate_checklist_score(self):
        """Calculate compliance score (percentage of 'Yes' items)."""
        if not self.audit_checklist:
            self.checklist_score = 0
            return

        total = len(self.audit_checklist)
        na_count = sum(1 for item in self.audit_checklist if item.complied == "NA")
        applicable = total - na_count

        if applicable == 0:
            self.checklist_score = 100
            return

        complied = sum(1 for item in self.audit_checklist if item.complied == "Yes")
        partial = sum(1 for item in self.audit_checklist if item.complied == "Partial")

        self.checklist_score = flt(((complied + (partial * 0.5)) / applicable) * 100, 2)
