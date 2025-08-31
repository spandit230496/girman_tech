# File: hrms_customization/hrms_customization/doctype/tax_regime_comparison_report/tax_regime_comparison_report.py
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Employee"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": _("Department"), "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 120},
        {"label": _("Gross Salary"), "fieldname": "gross_salary", "fieldtype": "Currency", "width": 120},
        {"label": _("Old Regime Tax"), "fieldname": "old_regime_tax", "fieldtype": "Currency", "width": 120},
        {"label": _("New Regime Tax"), "fieldname": "new_regime_tax", "fieldtype": "Currency", "width": 120},
        {"label": _("Tax Difference"), "fieldname": "tax_difference", "fieldtype": "Currency", "width": 120},
        {"label": _("Recommended Regime"), "fieldname": "recommended_regime", "fieldtype": "Data", "width": 120},
        {"label": _("Tax Saving"), "fieldname": "tax_saving", "fieldtype": "Currency", "width": 120}
    ]

def get_data(filters):
    data = []
    
    # Get all active employees
    employees = frappe.get_all("Employee",
        filters={"status": "Active"},
        fields=["name", "employee_name", "department", "custom_tax_regime_preference"]
    )
    
    for emp in employees:
        # Get employee salary details
        salary_details = get_employee_salary_details(emp.name)
        if not salary_details:
            continue
            
        # Calculate tax under both regimes
        old_regime_tax = calculate_tax_old_regime(salary_details["annual_gross"])
        new_regime_tax = calculate_tax_new_regime(salary_details["annual_gross"])
        
        # Compare and recommend
        tax_difference = new_regime_tax - old_regime_tax
        recommended = "Old Regime" if old_regime_tax < new_regime_tax else "New Regime"
        tax_saving = abs(tax_difference)
        
        data.append({
            "employee": emp.name,
            "employee_name": emp.employee_name,
            "department": emp.department,
            "gross_salary": salary_details["monthly_gross"],
            "old_regime_tax": old_regime_tax / 12,  # Monthly tax
            "new_regime_tax": new_regime_tax / 12,  # Monthly tax
            "tax_difference": tax_difference / 12,
            "recommended_regime": recommended,
            "tax_saving": tax_saving / 12
        })
    
    return data

def get_employee_salary_details(employee):
    """Get employee's gross salary"""
    latest_slip = frappe.get_all("Salary Slip",
        filters={"employee": employee, "docstatus": 1},
        fields=["gross_pay"],
        order_by="creation desc",
        limit=1
    )
    
    if latest_slip:
        return {
            "monthly_gross": latest_slip[0].gross_pay,
            "annual_gross": latest_slip[0].gross_pay * 12
        }
    return None