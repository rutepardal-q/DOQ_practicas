from odoo import models, fields, api, exceptions, _ 


class LibraryRental(models.Model):
    _name = "library.rental"
    _description = "Rental Information"


    rentedbook_ids = fields.Many2many(comodel_name='library.book', string='Rented Books', required=True, ondelete='cascade', domain="[('state', '=', 'renting')]")
    
       