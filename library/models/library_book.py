from odoo import models, fields, _ 

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "book_info"

    name = fields.Char(string = "Title", required=True)
    price = fields.Float(string = "Price")
    edition = fields.Integer(string = "Edition")
    book_type = fields.Selection(string="Type", selection = [("printed", "Printed"), ("digital", "Digital")])
    url = fields.Char(string="Url")
    is_purchased = fields.Boolean(string="Purchased", default= False)
    time_purchased = fields.Datetime(string = "Time Purchased")