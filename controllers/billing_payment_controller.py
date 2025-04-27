from models.billing_payment_model import InvoiceModel
 
class ManageInvoiceController:
     def __init__(self):
         self.invoice_model = InvoiceModel()
 
     def get_all_invoices(self):
         return self.invoice_model.get_all_invoices()
 
     def add_invoice(self, invoice_data):
         self.invoice_model.add_invoice(invoice_data)
 
     def update_invoice(self, invoice_data):
         self.invoice_model.update_invoice(invoice_data)
 
     def delete_invoice(self, invoice_id):
         self.invoice_model.delete_invoice(invoice_id)
 
     def search_invoices(self, conditions):
         return self.invoice_model.search_invoices(conditions)