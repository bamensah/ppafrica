from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError, ValidationError
import requests
import json
import phonenumbers
from datetime import datetime


class WizardFreeDay(models.TransientModel):
    _name = 'free.days.discount'
    _description = 'Free days and discount'

    delayed_days = fields.Integer('Free days', required=True)
    discounted_days = fields.Integer("Discounted days")
    note = fields.Char('Note')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    sale_order = fields.Many2one('sale.order', string='Sale Order')
    tag_ids = fields.Many2many('free.day.tag', string='Free Days Tags', required=True)

    # @api.multi
    # def name_get(self):
    #     res = []
    #     for rec in self:
    #         res.append((rec.id, ",".join(k.tag for k in rec.tag_ids)))
    #     return res
    #
    # @api.multi
    # def give_free_days(self, device_serial):
    #     params = self.env['ir.config_parameter'].sudo()
    #     API_GATEWAY_URL = params.get_param('api_gateway_url')
    #     API_GATEWAY_TOKEN = params.get_param('api_gateway_access_token')
    #     HEADERS = {
    #         "Content-Type": "application/json",
    #         "Authorization": "Bearer " + API_GATEWAY_TOKEN,
    #     }
    #
    #     URL = API_GATEWAY_URL + "/api/v1/" + self.env['account.payment'].get_country() + "/give_delay"
    #     data = {"delayed_days": self.delayed_days, "device_serial": device_serial}
    #     resp = requests.post(URL, data=json.dumps(data), headers=HEADERS)
    #     response = resp.json()
    #
    #     response_code = resp.status_code
    #     #TODO REPLACE BY TRY CATCH
    #     if str(response_code) == '200' or str(response_code)=='201':
    #         if 'error' in response:
    #             raise exceptions.Warning(_('PaygOps ERROR : ' + response["error_message"]))
    #         elif 'answer_data' in response:
    #             if len(response["answer_data"]) > 1:
    #                 if 'activation_answer_code' in response["answer_data"][1]:
    #                     token_code = response["answer_data"][1]["activation_answer_code"]
    #                     credit_end_date = response["answer_data"][1]["expiration_time_year"] + '-' + response["answer_data"][1]["expiration_time_month"] + '-' + response["answer_data"][1]["expiration_time_day"]
    #                     token_id = response["uuid"]
    #                     duration = response["answer_data"][0]["delayed_days"]
    #                     generated_date=response["time"]
    #                     token_type = response["type"]
    #                     client_id= response["answer_data"][0]["client_id"]
    #                     device_id = self.env['stock.production.lot'].search([('name', '=', device_serial)],limit=1)
    #
    #                     token = self.env['credit.token'].create({'code': token_code, 'token_id': token_id, 'duration': duration, 'token_type': token_type, 'credit_end_date': datetime.strptime(credit_end_date, '%Y-%m-%d'), 'generated_date': generated_date,
    #                         'inventory_id': device_id.id, 'transaction_id': '', 'payment_id': False, 'partner_id': self.invoice_id.partner_id.id, 'amount': False, 'device_serial': device_serial,
    #                         'salesperson': self.sale_order.user_id.id, 'loan_id': self.sale_order.id, 'phone_number': self.invoice_id.partner_id.phone,'phone_number_partner': self.invoice_id.partner_id.phone})
    #
    #                     self.sale_order.calculate_status()
    #
    #             else:
    #                 warning_message=''
    #                 if response["answer_data"][0]["status"] == 'NO_ACTIVATION_TIME_ON_DEVICE':
    #                     message_no_activation = ' Please register a payment for this client and the corresponding sale order to activate the device and generate a token.'
    #                 raise exceptions.Warning(_('PaygOps : ' + response["answer_data"][0]["status"] + message_no_activation))
    #         elif 'error_message' in response:
    #             raise exceptions.Warning(_('PaygOps ERROR : ' + response["error_message"]))
    #     else :
    #         if 'msg' in response:
    #             raise exceptions.Warning(_(response["msg"]))
    #         elif 'error' in response:
    #             raise exceptions.Warning(_(response["error"]))
    #         elif 'message' in response:
    #             raise exceptions.Warning(_('PaygOps ERROR : ' + response["message"]))
    #
    # def confirm_free_days(self):
    #     if self.delayed_days > 0:
    #         if self.invoice_id.payment_term_id and self.invoice_id.origin:
    #             sale_order = self.env['sale.order'].search(
    #                 [('name', '=', self.invoice_id.origin), ('partner_id', '=', self.invoice_id.partner_id.id)],
    #                 limit=1)
    #             if sale_order and sale_order.paygops_id.device_id:
    #                 self.write({'sale_order': sale_order.id})
    #                 self.env.cr.commit()
    #                 self.give_free_days(sale_order.paygops_id.device_id)
    #                 self.sale_order.free_days_taken += self.delayed_days
    #             else:
    #                 raise exceptions.Warning(_('There is no device registered for the client in PaygOps'))
    #     else:
    #         raise ValidationError("Please specify delayed days greater than 0")


class FreeDaysTags(models.TransientModel):
    _name = 'free.days.tags'
    _description = 'free days tags & description'

    # @api.multi
    # def unlink(self, values):
    #     tag_unlink = super(FreeDaysTags, self).unlink()
    #     return tag_unlink
