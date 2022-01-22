# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class sale_order_inherit(models.Model):
    _inherit = 'sale.order'
    
    compute_account_number = fields.Char(string="Computed Account Number", compute='_compute_account_number' )
    
    account_number = fields.Char(string="Stored Account Number", store=True ) #compute='_store_account_number'
    
    origin = fields.Char(string='Account Number')
    
    # @api.depends('compute_account_number')
    # def _store_account_number(self):
    #     for record in self:
    #         _logger.info("Recording account number")
    #         record.account_number = record.compute_account_number
    
    @api.depends('invoice_status')
    def _compute_account_number(self):
        for s in self:
            if(s.invoice_status == 'invoiced'):
                stock_picked = s.picking_ids
                stock_picking_states = ['assigned', 'first_done', 'done']
                if s.paygops_id:
                    if (any(picked.state in stock_picking_states for picked in stock_picked)):
                        stock_move_lines = self.env['stock.move.line'].search_read([('picking_id','in',stock_picked.ids),('product_id.name', 'ilike', '%Battery%')], ['lot_id', 'product_id'])
                        all_serials = list(map(lambda z: z[1], filter(lambda y: y != False ,map(lambda x: x['lot_id'], stock_move_lines))))                       
                        if(any(all_serials)):
                            s.compute_account_number = all_serials[0].replace('OPT-PL', 'PL')

    
    @api.onchange('product_template_id')
    def onchange_product_template(self):
        for s in self:
            if s.product_template_id:
                s.payment_term_id = s.product_template_id.payment_term_id.id
                if s.product_template_id.type_of_product_id:
                    s.type_of_product_id = s.product_template_id.type_of_product_id.id
                    
                    
    @api.onchange('user_id')
    def onchange_salesperson_set_team(self):
        for s in self:
            if s.user_id:
                salesperson_team = self.env['crm.team'].search([
                    ('member_ids', 'in', s.user_id.id)
                    ], limit=1)
                
                s.team_id = salesperson_team.id