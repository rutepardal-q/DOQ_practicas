from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")

   

    # Type of Contact

    is_member = fields.Boolean(string="Member", default=False )
    is_author = fields.Boolean(string="Author", default=False )
    is_commercial = fields.Boolean(string='Commercial', default=False)

    #Members
    member_id = fields.Char(string="Member Number")
    
    rented_books_count = fields.Integer(
        string='Rented Books Count', 
        compute='_compute_rented_books',
        store= False)
    rented_books = fields.One2many(
        'library.book', 
        'renting_member', 
        string='Rented Books', 
        compute='_compute_rented_books',
        store=False
        )


    @api.depends('rented_books')
    def _compute_rented_books(self):
        for member in self:
            rented_books = member.rented_books.filtered(lambda book: book.state == 'renting')
            member.rented_books_count = len(member.rented_books)
            member.rented_books = rented_books


    def action_show_rented_books(self):
        if self:
            self.ensure_one()
            return {
                'name': 'Rented Books',
                'type': 'ir.actions.act_window',
                'res_model': 'library.book',
                'view_mode': 'tree',
                'view_id': self.env.ref('library.book_view_tree').id,
                'domain': [('renting_member', '=', self.id)],
                'target': 'current',
                'flags': {
                    'create': False,
                    'delete': False,
                },
            }


    #Authors
    genre_ids = fields.Many2many(comodel_name='library.genre', string="Genres")
    book_ids = fields.One2many(
        comodel_name='library.book', 
        inverse_name='author_id') 
    
    
    #Full Name
    @api.onchange('first_name', 'last_name')
    def _compute_full_name(self):
        self.name = ''
        if self.first_name:
            self.name += self.first_name
        if self.last_name:
            self.name += ' ' + self.last_name
    
    #Commercials
    commercial_code = fields.Char(copy=False)
    commission = fields.Float(string='% Commission')

    _sql_constraints = [
        ('commercial_code_uniq', 'unique (commercial_code)',
         'The commercial code must be unique!')
    ]

        # Not deleting Commercials
    
    def unlink(self):
        # Mapped itera sobre un recordset para agrupar un campo en una lista
        if any(self.mapped('commercial_code')):
            raise UserError("You can not delete a contact with"
                            " a Commercial Code")
        res = super().unlink()
        return res