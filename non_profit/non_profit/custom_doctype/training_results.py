# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document

from erpnext.setup.doctype.employee.employee import get_employee_emails



def validate(self):
    training_event = frappe.get_doc("Training Event", self.training_event)
    if training_event.docstatus != 1:
        frappe.throw(_("{0} must be submitted").format(_("Training Event")))

    self.member_emails = ", ".join(get_employee_emails([d.member for d in self.members]))

def on_submit(self):
    training_event = frappe.get_doc("Training Event", self.training_event)
    training_event.status = "Completed"
    for m in self.employees:
        for m1 in training_event.employees:
            if m1.member == m.member:
                m1.status = "Completed"
                break

    training_event.save()
@frappe.whitelist()
def get_employees(training_event):
	return frappe.get_doc("Training Event", training_event).employees