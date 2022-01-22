# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountInvoiceInherit(models.Model):
    _inherit = "account.move"
    #_inherit = "account.invoice"

    # needs to open

    def action_post(self):
        for invoice in self.filtered(lambda invoice: invoice.partner_id not in invoice.message_partner_ids):
            invoice.message_subscribe([invoice.partner_id.id])
   
             # Auto-compute reference, if not already existing and if configured on company
             # if not invoice.reference and invoice.type == 'in_invoice':
             #     invoice.reference = invoice._get_computed_reference()
            if not invoice.payment_reference and invoice.move_type == 'in_invoice':
                 # invoice.payment_reference = invoice._get_computed_reference()
                invoice.payment_reference = invoice._get_invoice_computed_reference()
        self._check_duplicate_supplier_reference()
    
         # add by khk
        for invoice in self:
            for invoice_line in invoice.invoice_line_ids:
                if invoice_line.landed_cost_line_origin:
                    invoice_line.landed_cost_line_origin.write({'invoiced': True})
         #self.write({'state': 'post'})
    
        return super(AccountInvoiceInherit, self).action_post()


class AccountInvoiceLoineInherit(models.Model):
    _inherit = "account.move.line"
    #_inherit = "account.invoice.line"

    landed_cost_line_origin = fields.Many2one('stock.landed.cost.lines')
