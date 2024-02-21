
from odoo import models, fields, _ 


class LibraryAudit(models.Model):
    _name = 'library.audit'
    _description = 'Audit'

    operation = fields.Selection(string='Operation', selection=[('create', 'Create'), ('write', 'Write'), ('unlink', 'Unlink')])
    user_id = fields.Char(string='User ID')
    date = fields.Datetime(string='Date')
    res_id = fields.Integer(string='Resource ID')
    res_mod = fields.Char(string='Resource Model')
    
    # book_id = fields.Char(string='Book ID')
    

