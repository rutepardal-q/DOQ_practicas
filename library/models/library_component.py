
from odoo import models, fields, _ 

class LibraryComponent(models.Model):
    _name = 'library.component'
    _description = 'Library Book Component Line'

    name = fields.Char(string="Component", required=True)

    pack_id = fields.Many2one(comodel_name='library.book', string='Pack')
    
    
    