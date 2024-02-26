from odoo import models, fields, api, exceptions, _ 


class LibraryRental(models.Model):
    _name = "library.rental"
    _description = "Rental Information"

    renting_member = fields.Many2one(comodel_name='res.partner', string='Member',required=True, ondelete='cascade', domain="[('is_member', '=', True)]")
    rented_book = fields.Many2one('library.book', string='Book')
    start_date = fields.Datetime(string='Rental Date')
    maxend_date = fields.Datetime(string='Return Before')
    end_date = fields.Datetime(string='Return Date')
    rental_state = fields.Selection([('available', 'Available'),('pending', 'Pending Return'), ('returned', 'Returned')], default='pending')

