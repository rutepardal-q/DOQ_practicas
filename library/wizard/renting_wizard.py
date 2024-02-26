import datetime
from odoo import models, fields, api, _


class RentingWizard(models.TransientModel):
    _name ='library.renting.wizard'
    _description = 'Rent Books'

    renting_member = fields.Many2one('res.partner', string='Member', required=True, domain="[('is_member', '=', True)]")
    rented_book = fields.Many2one('library.book', string='Book', required=True)

    start_date = fields.Date(string='Rental Date', required=True, default=fields.Datetime.now, readonly=True)
    maxend_date = fields.Date(string='Return before', required=True, default=lambda self: fields.Datetime.now() + datetime.timedelta(weeks=3), readonly=True)

    rental_id = fields.Many2one('library.rental', string='Rental', required=True)
    end_date = fields.Datetime(related='rental_id.end_date', string='Return Date', readonly=True)
    # end_date = fields.Date(string='Return Date', readonly=True)

   
   
    def action_confirm_renting_button(self):
        # Check if there are no more than one pending rentals for this partner
        pending_rentals = self.env['library.rental'].search([
            ('renting_member', '=', self.renting_member.id),
            ('rental_state', '=', 'pending'),
        ])
        
        if len(pending_rentals) < 2:
            # Create a new rental record
            rental_vals = {
                'renting_member': self.renting_member.id,
                'rented_book': self.rented_book.id,
                'start_date': self.start_date,
                'maxend_date': self.maxend_date,
            }
            self.env['library.rental'].create(rental_vals)
            
            # You can add additional logic here, such as updating book availability, etc.
            
            return {'type': 'ir.actions.act_window_close'}
        else:
            # Handle the case where there are already two pending rentals
            # You can add a warning or custom logic as needed
            return {
                'name': 'Warning',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_id': self.env.ref('library.warning_2rent_wizard_form').id,  
                'target': 'new',
            }