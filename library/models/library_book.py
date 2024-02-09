from odoo import models, fields, api, exceptions, _ 

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Book Information"

    _inherits = {'product.product': 'product_id', 'res.partner':'contact_id'}


    name = fields.Char(string="Name", required=True)
    price = fields.Float(string="Price")
    edition = fields.Integer(string="Edition")
    is_book= fields.Boolean(string="Book", default= True, readonly= True)
    book_type = fields.Selection(
        string="Type", 
        selection = [("printed", "Printed"), ("digital", "Digital")]
        )
    url = fields.Char(string="URL")
    is_purchased = fields.Boolean(
        string="Purchased", 
        default= False
        )
    time_purchased = fields.Datetime(string = "Time Purchased")
    is_pack = fields.Boolean(string='Pack')
    pack = fields.Selection(
        string='Type of Pack', 
        selection=[('collection', 'Collection'), ('series', 'Series')]
        )
    
    
    product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='cascade')
    contact_id = fields.Many2one('res.partner', string='Author', required=True, ondelete='cascade', domain="[('is_author', '=', True)]")
    genre_id = fields.Many2many(comodel_name='library.genre', string='Genre', required=True, ondelete='cascade')
    component_ids = fields.One2many(comodel_name='library.component', inverse_name='pack_id', string='Components')
    
    
    @api.onchange("is_pack")
    def _onchange_is_pack(self):
        if self.is_pack:
            self.pack = "collection"
        if not self.is_pack:
            self.pack = ""

    def create(self, values):
        newbook = super(LibraryBook, self).create(values)

        audit_values = {
            'user_id': self.env.user.id,
            'date': fields.Datetime.now(),
            'operation': 'create',
            'book_id': newbook.id,
            }
        self.env['library.audit'].create(audit_values)

        return newbook 

    def write(self, values):
        chbook = super(LibraryBook, self).write(values)
        audit_values = {
            'user_id': self.env.user.id,
            'date': fields.Datetime.now(),
            'operation': 'write',
            'book_id': self.id,
        }
        self.env['library.audit'].create(audit_values)

        return chbook
    
    def unlink(self):
        delbook = super(LibraryBook, self).unlink()
        audit_values = {
            'user_id': self.env.user.id,
            'date': fields.Datetime.now(),
            'operation': 'unlink',
            'book_id': self.id,
        }
        self.env['library.audit'].create(audit_values)

        return delbook
    
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise exceptions.ValidationError("The price should be positive!")