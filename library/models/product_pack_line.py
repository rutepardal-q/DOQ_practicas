### PART OF PRACICAS EXTRA, IMPLEMENT ONLY IF NECESSARY FOR FOLLOWIN EXERCISES

"""

from odoo import api, fields, models


class ProductPackLine(models.Model):
    _name = 'product.pack.line'
    pack_id = fields.Many2one(
        comodel_name='product.product',
        string="Pack",
    )
    component_id = fields.Many2one(
        comodel_name='product.product',
        string="Component",
        required=True,
    )
    quantity = fields.Integer(
        string="Quantity",
    )
    price = fields.Float(
        string="Price",
    )

    @api.onchange('component_id')
    def onchange_component_id(self):
        self.price = self.component_id.list_price """