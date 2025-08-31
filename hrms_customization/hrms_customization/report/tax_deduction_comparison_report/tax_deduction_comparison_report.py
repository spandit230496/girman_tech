# File: hrms_customization/hrms_customization/report/tax_regime_comparison_report/tax_regime_comparison_report.py
import frappe
from frappe import _
from frappe.utils import flt

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
        {"label": _("Recommended"), "fieldname": "recommended_regime", "fieldtype": "Data", "width": 100},
        {"label": _("Tax Saving"), "fieldname": "tax_saving", "fieldtype": "Currency", "width": 120}
    ]

def get_data(filters):
    data = []
    
    # Get employees with optional department filter
    employee_filters = {"status": "Active"}
    if filters.get("department"):
        employee_filters["department"] = filters.get("department")
    
    employees = frappe.get_all("Employee",
        filters=employee_filters,
        fields=["name", "employee_name", "department"]
    )
    
    for emp in employees:
        gross_salary = get_employee_gross_salary(emp.name)
        if not gross_salary:
            continue
            
        annual_gross = gross_salary * 12
        
        # Calculate taxes using local functions
        old_tax = calculate_old_regime_tax(annual_gross)
        new_tax = calculate_new_regime_tax(annual_gross)
        
        tax_diff = new_tax - old_tax
        recommended = "Old Regime" if old_tax < new_tax else "New Regime"
        tax_saving = abs(tax_diff)
        
        data.append({
            "employee": emp.name,
            "employee_name": emp.employee_name,
            "department": emp.department,
            "gross_salary": gross_salary,
            "old_regime_tax": old_tax / 12,  # Monthly
            "new_regime_tax": new_tax / 12,  # Monthly
            "tax_difference": tax_diff / 12,
            "recommended_regime": recommended,
            "tax_saving": tax_saving / 12
        })
    
    return data

def get_employee_gross_salary(employee):
    """Get latest gross salary from salary slip"""
    latest_slip = frappe.get_all("Salary Slip",
        filters={"employee": employee, "docstatus": 1},
        fields=["gross_pay"],
        order_by="creation desc",
        limit=1
    )
    return latest_slip[0].gross_pay if latest_slip else 0

def calculate_old_regime_tax(annual_income):
    """Old regime tax calculation with standard deduction"""
    # Standard deduction of ₹50,000
    taxable_income = max(0, annual_income - 50000)
    
    tax = 0
    if taxable_income > 1000000:
        tax = 112500 + (taxable_income - 1000000) * 0.30
    elif taxable_income > 500000:
        tax = 12500 + (taxable_income - 500000) * 0.20
    elif taxable_income > 250000:
        tax = (taxable_income - 250000) * 0.05
    
    # Add 4% health and education cess
    tax += tax * 0.04
    
    return tax

def calculate_new_regime_tax(annual_income):
    """New regime tax calculation (no deductions)"""
    tax = 0
    if annual_income > 1500000:
        tax = 187500 + (annual_income - 1500000) * 0.30
    elif annual_income > 1200000:
        tax = 90000 + (annual_income - 1200000) * 0.20
    elif annual_income > 900000:
        tax = 45000 + (annual_income - 900000) * 0.15
    elif annual_income > 600000:
        tax = 15000 + (annual_income - 600000) * 0.10
    elif annual_income > 300000:
        tax = (annual_income - 300000) * 0.05
    
    # Add 4% health and education cess
    tax += tax * 0.04
    
    return tax