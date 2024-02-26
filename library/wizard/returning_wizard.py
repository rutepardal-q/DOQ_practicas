from odoo import models, fields, api, _


class ReturningWizard(models.TransientModel):
    _name ='library.returning.wizard'
    _description = 'Return Books'

    rented_book = fields.Many2one('library.book', string='Book', required=True,  domain="[('rental_state', '=', 'pending')]")
    renting_member = fields.Many2one('res.partner', string='Member', required=True, domain="[('is_member', '=', True)]")


    end_date = fields.Datetime(string='Return Date', required=True, default=fields.Datetime.now, readonly=True)

    def action_confirm_returning_button(self):
        # Check if there are no more than one pending rentals for this partner
        rental_record = self.env['library.rental'].search([
            ('rented_book', '=', self.rented_book.id),
            ('renting_member', '=', self.renting_member.id),
            ('rental_state', '=', 'pending'),
        ], limit=1)
        #change status
        if rental_record:
            rental_record.write({
                'rental_state': 'returned',
                'end_date': self.end_date
            })
            return {'type': 'ir.actions.act_window_close'}
        else:
            return {
                'warning': {
                    'title': _('Warning'),
                    'message': _('This book is not marked as "Pending Return" for the selected member.'),
                }
            }
