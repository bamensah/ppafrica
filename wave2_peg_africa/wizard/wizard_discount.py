import requests
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

TYPE = [
    ('free_days', 'Free days'),
    ('amount', 'Amount'),
]


class WizardFreeDay(models.TransientModel):
    _name = 'wave.peg.africa.discount'
    _description = 'Discount'

    # @api.onchange('type')
    # def _reset_days_or_amount(self):
    #     if not self.type:
    #         self.days = 0
    #         self.amount = 0.0
    #     elif self.type == 'free_days':
    #         self.amount = 0.0
    #     else:
    #         self.days = 0
    #     return

    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    type = fields.Selection(TYPE, required=True)
    days = fields.Integer('Free days', store=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.user.company_id.id)
    tag_id = fields.Many2one('discount.tag', string='Discount Tags', required=True)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, \
                                  default=lambda self: self.env.user.company_id.currency_id.id, store=True)
    amount = fields.Monetary('Amount')

    # def action_confirm(self):
    #     invoice_id = self.env.context.get('invoice_id', False)
    #     if not invoice_id:
    #         raise UserError("This invoice doesn't exist!")
    #     self.invoice_id = self.env["account.invoice"].browse(invoice_id)
    #     if (not self.invoice_id.paygops_id) and (self.type == 'free_days'):
    #         raise UserError("You can just choose Amount")
    #     sale_order = self.invoice_id.sale_order_id
    #     ref_pricing_amount = 0
    #     account_analytic_id = False
    #
    #     if self.days:
    #         minimum_amount_days = sale_order.payment_term_id.minimum_amount_days
    #         minimum_amount_value = sale_order.payment_term_id.minimum_amount_value
    #         if minimum_amount_days:
    #             ref_pricing_amount = self.days * (minimum_amount_value / minimum_amount_days)
    #     elif self.amount:
    #         ref_pricing_amount = self.amount
    #     else:
    #         pass
    #     if ref_pricing_amount:
    #         product = self.tag_id.product_id
    #         account_id = self.tag_id.account_id.id
    #         journal_id = self.tag_id.journal_id.id
    #         discount_tax_id = self.tag_id.tax_id.id if self.tag_id.tax_id else self.env['account.tax'].search([
    #             ('name', '=', 'TVA Discount'),
    #             ('company_id', '=', self.env.user.company_id.id)
    #         ], limit=1).id
    #         account_analytic_id = self.invoice_id.invoice_line_ids[0].account_analytic_id
    #         credit_note = self.env['account.invoice'].create({
    #             'type': 'out_refund',
    #             'partner_id': sale_order.partner_id.id,
    #             'origin': sale_order.name,
    #             'date_invoice': fields.Date.context_today(self),
    #             'journal_id': journal_id,
    #             'invoice_line_ids': [(0, 0, {
    #                 'product_id': product.id,
    #                 'name': product.name,
    #                 'account_id': account_id,
    #                 'account_analytic_id': account_analytic_id.id if account_analytic_id else False,
    #                 'price_unit': ref_pricing_amount,
    #                 'invoice_line_tax_ids': [(4, discount_tax_id)],
    #             })]
    #         })
    #
    #         #W2E-280 Credit note comes in draft state
    #         credit_note.action_credit_note_draft()
    #
    #         sale_order.write({
    #             'outstanding_balance': sale_order.payment_term_id.financed_price - sale_order.total_amount_paid - sale_order.discount_given
    #         })
    #         params = self.env['ir.config_parameter'].sudo()
    #         API_GATEWAY_URL = params.get_param('api_gateway_url')
    #         API_GATEWAY_TOKEN = params.get_param('api_gateway_access_token')
    #         HEADERS = {
    #             "Content-Type": "application/json",
    #             "Authorization": "Bearer " + API_GATEWAY_TOKEN,
    #         }
    #         country = self.env['account.payment'].get_country()
    #         if sale_order.paygops_id:
    #             # Créer une nouvelle offre PAYGOPS
    #             offer_id = sale_order.payment_term_id.paygops_offer_id
    #             new_amount = sale_order.payment_term_id.financed_price - ref_pricing_amount
    #             URL = API_GATEWAY_URL + "/api/v1/" + country + "/offers/" + str(offer_id) + "/" + str(new_amount) + "/" + sale_order.name
    #             resp = requests.put(URL, headers=HEADERS)
    #             response = resp.json()
    #             if resp.status_code == 400:
    #                 return False
    #             # Lier le client à la nouvelle offre
    #             offer_code = response['code']
    #             offer_id = response['id']
    #             offer_name = response['name']
    #             device_serial = sale_order.paygops_id.device_id
    #             URL = API_GATEWAY_URL + "/api/v1/" + country + "/change_offer/" + str(device_serial) + "/" + str(
    #                 offer_code)
    #             resp = requests.get(URL, headers=HEADERS)
    #             response = resp.json()
    #             if not response['success']:
    #                 return False
    #             #Créer un specific payment terms en changeant l'offer ID et le name
    #             new_payment_term_id = sale_order.payment_term_id.sudo().copy({
    #                 'name': offer_name,
    #                 'paygops_offer_id': offer_id,
    #             })[0]
    #             sale_order.payment_term_id = new_payment_term_id
    #
    #     return True
