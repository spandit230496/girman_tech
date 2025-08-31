# File: hrms_customization/hrms_customization/override.py
import frappe
from frappe.model.document import Document
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip as BaseSalarySlip

class CustomSalarySlip(BaseSalarySlip):
    def validate(self):
        # First call parent's validate method
        super().validate()
        
        # NOW apply investment exemption
    #     self.apply_investment_exemption()
    
    # def apply_investment_exemption(self):
    #     """Apply investment exemption to reduce taxable income"""
    #     if self.custom_investment_declaration:
    #         # Get total exemption amount from declaration
    #         total_exemption = frappe.db.get_value(
    #             "Employee Investment Declaration", 
    #             self.custom_investment_declaration,  # This is the document name
    #             "total_exemption"
    #         )
            
    #         # Check if document is submitted separately
    #         docstatus = frappe.db.get_value(
    #             "Employee Investment Declaration", 
    #             self.custom_investment_declaration, 
    #             "docstatus"
    #         )
            
    #         if total_exemption and docstatus == 1:  # Only if submitted
    #             # Reduce taxable income by exemption amount
    #             self.taxable_income = max(0, self.taxable_income - total_exemption)
                
