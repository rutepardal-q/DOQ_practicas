from odoo import models, fields, api, exceptions, _ 

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Book Information"

    _inherits = {'product.product': 'product_id'}
    _inherit = ['library.audit.mixing', 'mail.thread', 'mail.activity.mixin']


# Book basics
    synopsis = fields.Html(string='Synopsis')
    year = fields.Integer(string='Published in')
    edition = fields.Integer(string="Edition")
    barcode = fields.Char(string='ISBN')
    book_type = fields.Selection(
        string="Type", 
        selection = [("printed", "Printed"), ("digital", "Digital")]
        )
    url = fields.Char(string="URL")
    is_purchased = fields.Boolean(
        string="Purchased", 
        default= False
        )
    time_purchased = fields.Datetime(string="Time Purchased")
    


    # Connection to Products
    product_id = fields.Many2one('product.product', string='Product', auto_join=True, required=True, ondelete='cascade')

    # Connection to Contacts: Authors
    author_id = fields.Many2one(
        'res.partner', 
        string='Author', 
        required=True, 
        ondelete='cascade', 
        domain="[('is_author', '=', True)]"
        )
    
   #GENRE
    genre_ids = fields.Many2many(
        comodel_name='library.genre', 
        string='Genres', 
        required=True, 
        ondelete='cascade',
        )



    # Dealers and Editorial Line
    dealer_line_ids = fields.One2many(
        comodel_name='library.dealer.line',
        inverse_name='book_id', string='Dealers')
    editorial_line_ids = fields.One2many(
        comodel_name='books.editorial.line',
        inverse_name='book_id', string='Editorial')
    
    # Packs and their components

    is_pack = fields.Boolean(string='Pack')
    pack = fields.Selection(
        string='Type of Pack', 
       selection=[('collection', 'Collection'), ('series', 'Series')]
    )
     
    component_ids = fields.One2many(
        comodel_name='library.component', 
        inverse_name='pack_id', 
        string='Components')
    
    @api.onchange("is_pack")
    def _onchange_is_pack(self):
        if self.is_pack:
            self.pack = "collection"
        if not self.is_pack:
            self.pack = ""
    
    # Price must be positive
    @api.constrains('list_price')
    def _check_price(self):
        for record in self:
            if record.list_price < 0:
                raise exceptions.ValidationError("The price should be positive!")
            
    # RENTING
    
    # State
    state = fields.Selection(
        selection=[('in_stock', 'In Stock'),
                ('renting', 'Renting'),
                ('lost', 'Lost')], 
                required=True,
                default= "in_stock")

    available = fields.Boolean(compute="_compute_available", store=True)

    # Avalable only when In Stock
    @api.depends('state')
    def _compute_available(self):
        for rec in self:
            rec.available = rec.state == "in_stock"
    
    #Dates and members
            
    @api.onchange('state')
    def _onchange_state(self):
        for rec in self:
            if rec.state == 'in_stock':
                rec.return_date = fields.Datetime.now()
            elif rec.state == 'renting':
                rec.return_date = False

    renting_member = fields.Many2one('res.partner', string='Renting Member', required=True, ondelete='cascade', domain="[('is_member', '=', True)]")        
    
    last_renting_date = fields.Datetime(string='Last Renting')
    
   
    
    rental_date = fields.Datetime(string='Rental Date', default=fields.Datetime.now)
    return_date = fields.Datetime(string='Return Date')



    # AUDIT BOOKS

    #New book
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'barcode' in vals and vals['barcode']:
                if self.search([('barcode', '=', vals['barcode'])]):
                    raise exceptions.UserError("There is a book with the same ISBN %s" %
                                    vals['barcode'])
                if len(vals['barcode']) != 13:
                    raise exceptions.UserError("The ISBN must to have 13 characters")        
        # newbooks = super().create(vals_list)
        # for newbook in newbooks:
        #     audit_values = {
        #         'user_id': self.env.user.id,
        #         'date': fields.Datetime.now(),
        #         'operation': 'create',
        #         'book_id': newbook.id,
        #         }
        #     self.env['library.audit'].create(audit_values)

        # return newbooks 
    
    # Change
    def write(self, values):
        if values.get('state') and values.get('state') == 'renting':
            values['last_renting_date'] = fields.Datetime.now()
        if 'barcode' in values and values['barcode']:
                if self.search([('barcode', '=', values['barcode'])]):
                    raise exceptions.UserError("There is a book with the same ISBN %s" %
                                    values['barcode'])
                if len(values['barcode']) != 13:
                    raise exceptions.UserError("The ISBN must to have 13 characters")       
        # chbook = super(LibraryBook, self).write(values)
        # audit_values = {
        #     'user_id': self.env.user.id,
        #     'date': fields.Datetime.now(),
        #     'operation': 'write',
        #     'book_id': self.id,
        # }
        # self.env['library.audit'].create(audit_values)

        # return chbook
    
        #Delete
    # def unlink(self):
    #     delbook = super(LibraryBook, self).unlink()
    #     audit_values = {
    #         'user_id': self.env.user.id,
    #         'date': fields.Datetime.now(),
    #         'operation': 'unlink',
    #         'book_id': self.id,
    #     }
    #     self.env['library.audit'].create(audit_values)

    #     return delbook