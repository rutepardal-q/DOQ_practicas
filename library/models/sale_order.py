
from odoo import models, fields, api, exceptions, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    #_inherit = 'sale.order.line'

       # Only sell to members
    def action_confirm(self):
        for order in self:
            # Importing the necessary model within the method to avoid circular import
            from . import res_partner

            # Check if the customer has the "is_member" checkbox marked
            if order.partner_id and not order.partner_id.is_member:
                raise exceptions.UserError("You can only sell to members.")

            # Continue with the original action_confirm logic or add your modifications
            res = super(SaleOrder, order).action_confirm()

            # Add any additional logic here if needed

        return res

     # PART OF PRATICAS SOLUTIONS, ONLY IMPLEMENT IF NECESSARY FOR NEW EXERCISES
    #Pack components on Sales Orders
    """@api.onchange('product_id')
    def product_id_change(self):
        res = super().product_id_change()
        if self.product_id and self.product_id.is_pack and \
           self.product_id.component_line_ids:
            self.name += _('\n-- Components --')
            for line in self.product_id.component_line_ids:
                self.name += '\n %s - %i' % (line.component_id.name,
                                             line.quantity)
        return res
"""