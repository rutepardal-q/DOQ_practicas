from odoo import api, fields, models


class LibraryDealerLine(models.Model):
    _name = 'library.dealer.line'
    _description = 'New Description'

    dealer_id = fields.Many2one(comodel_name='res.partner')
    price_unit = fields.Float(string='')
    sale_unit = fields.Integer(string='Unit Sales')
    book_id = fields.Many2one(comodel_name='library.book')