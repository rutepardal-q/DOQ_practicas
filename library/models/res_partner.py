from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")

    #Full Name
    @api.onchange('first_name', 'last_name')
    def _compute_full_name(self):
        self.name = ''
        if self.first_name:
            self.name += self.first_name
        if self.last_name:
            self.name += ' ' + self.last_name

    # TYPE OF CONTACT

    is_member = fields.Boolean(string="is Member", default=False )
    is_author = fields.Boolean(string="is Author", default=False )
    is_commercial = fields.Boolean(string='is Commercial', default=False)

    #MEMBERS
    
    # Sequence for member number generation
    member_id = fields.Char(string="Member Number", copy=False, default='New', readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('member_id','New') =='New':
            vals['member_id'] = self.env['ir.sequence'].next_by_code('task.abdc') or 'New'

        result = super(ResPartner, self).create(vals)
        return result




    # renting_member_ids = fields.One2many(
    #     comodel_name='library.book', 
    #     inverse_name='renting_member') 


    # rented_books_count = fields.Integer(
    #     string='Rented Books Count', 
    #     compute='_compute_rented_books',
    #     store= False)
    # rented_books = fields.One2many(
    #     'library.book', 
    #     'renting_member', 
    #     string='Rented Books', 
    #     compute='_compute_rented_books',
    #     store=False
    #     )


    # @api.depends('rented_books')
    # def _compute_rented_books(self):
    #     for member in self:
    #         rented_books = member.rented_books.filtered(lambda book: book.state == 'renting')
    #         member.rented_books_count = len(member.rented_books)
    #         member.rented_books = rented_books


    def action_show_rented_books(self):
        if self and self.is_member:
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

    #Deactivate Members - open Wizard
        

    def action_deactivate_members_wizard(self):
        if self and self.is_member:
            self.ensure_one()
            context = {'default_active_id': self.id}
            return {
                'name': 'Deactivate Membership',
                'type': 'ir.actions.act_window',
                'res_model': 'library.deactivate.members.wizard',
                'view_mode': 'form',
                'view_id': self.env.ref('library.deactivate_members_wizard_view_form').id,
                'target': 'new',
                'context': context,
            }
   



    #AUTHORS
    genre_ids = fields.Many2many(comodel_name='library.genre', string="Genres")
    book_ids = fields.One2many(
        comodel_name='library.book', 
        inverse_name='author_id',
        compute='_compute_available_books',
        store=False) 
    
    available_books = fields.One2many(
        'library.book', 'author_id',
        string="Available Books", 
        compute='_compute_available_books', 
        store=False)
    
    total_sales_amount = fields.Integer(
        string='Sold Books',
        compute='_compute_total_sales_amount',
        compute_sudo=True,
        store=False 
    )

    total_sales_amount_text = fields.Char(
        string='Sold Books Text',
        compute='_compute_display_text',
        store=False
        )



    # @api.depends('book_ids')
    # def _compute_available_books(self):
    #     for author in self:
    #         # Find all rented books by the author
    #         rented_books = author.book_ids.filtered(lambda book: book.state == 'renting')
    #         # Filter books that are not in the list of rented books
    #         available_books = author.book_ids - rented_books

    #         # Set the result in the computed Many2one field
    #         author.available_books = available_books # and available_books[0] or False

    def action_show_available_books(self):
        if self and self.is_author:
            self.ensure_one()
            return {
                'name': 'Available Books',
                'type': 'ir.actions.act_window',
                'res_model': 'library.book',
                'view_mode': 'tree',
                'view_id': self.env.ref('library.book_view_tree').id,
                'domain': [('author_id', '=', self.id)],
                'target': 'current',
                'flags': {
                    'create': False,
                    'delete': False,
                },
            }
    def _compute_total_sales_amount(self):
        for author in self:
            # Find all books by the author
            author_books = self.env['library.book'].search([('author_id', '=', author.id)])

            #amounts_recordset = product_tmpl_id.sales_amount

            # Use mapped to get the total sales amount from the recordset of books
            total_sales_amount = sum(author_books.mapped('product_id.sales_count'))

            # Set the result in the computed field
            author.total_sales_amount = total_sales_amount

    @api.depends('total_sales_amount', 'total_sales_amount_text')
    def _compute_display_text(self):
        for rec in self:
            rec.total_sales_amount_text = f'Sold Books: {rec.total_sales_amount}'



    
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