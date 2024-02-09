
from odoo import models, fields, _ 


class LibraryGenre(models.Model):
    _name = 'library.genre'
    _description = 'Genre'

    name = fields.Char(string="Genre")


    
