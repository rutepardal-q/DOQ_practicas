
from odoo import models, fields, api, _


class Warning2RentWizard(models.TransientModel):
    _name ='library.warning.2rent.wizard'
    _description = 'Warning 2 books rented to same member'

    message = fields.Text(string="Warning: This partner already has two pending rentals.", readonly=True, store=True)