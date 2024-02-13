from odoo import models, fields, api

class BookSaleOrderReport(models.Model):
    _inherit = 'sale.report_saleorder'
    _description = 'Books Sale Order Report'

    member_id= fields.Char(string='Partner Number', compute='_compute_partner_number')

    @api.depends('partner_id')
    def _compute_partner_number(self):
        for order in self:
            order.partner_number = order.partner_id.ref if order.partner_id.is_company else ''
