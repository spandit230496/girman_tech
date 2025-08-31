# File: employee_investment_declaration.py
import frappe
from frappe.model.document import Document
from frappe import _

class EmployeeInvestmentDeclaration(Document):
    def validate(self):
        # Calculate totals
        self.total_80c = sum([d.amount or 0 for d in self.section_80c_investments])
        self.total_80d = sum([d.amount or 0 for d in self.section_80d_investments])
        self.total_other = sum([d.amount or 0 for d in self.other_exemptions])
        self.total_exemption = self.total_80c + self.total_80d + self.total_other
        
        # Calculate remaining limits
        self.remaining_80c = 150000 - self.total_80c
        self.remaining_80d = 100000 - self.total_80d
        
        # Check limits
        if self.total_80c > 150000:
            frappe.throw("80C limit is ₹1,50,000")
            
        if self.total_80d > 100000:
            frappe.throw("80D limit is ₹1,00,000")
    
    def on_submit(self):
        # Update employee record
        frappe.db.set_value("Employee", self.employee, "custom_investment_declaration", self.name)
    
    def on_cancel(self):
        # Clear from employee record
        frappe.db.set_value("Employee", self.employee, "custom_investment_declaration", "")

@frappe.whitelist()
def get_tax_declaration(employee, year):
    # Get declaration for payroll
    decl = frappe.get_all("Employee Investment Declaration",
        filters={"employee": employee, "financial_year": year, "docstatus": 1},
        fields=["total_exemption", "total_80c", "total_80d", "total_other"],
        limit=1
    )
    return decl[0] if decl else None