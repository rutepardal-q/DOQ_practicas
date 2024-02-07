from odoo import models, fields, api, _ 

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

        
    
