
from odoo import models, fields, _ 


class LibraryBookGenre(models.Model):
    _name = 'library.bookgenre'
    _description = 'genre'

    name = fields.Char(string="Genre")
    
