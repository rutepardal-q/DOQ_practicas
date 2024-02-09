
from odoo import models, fields, api, exceptions, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

   # @api.multi
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


