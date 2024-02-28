# from odoo import models, fields, api, exceptions, _ 

# class LibrarySettings(models.Model):
#     _name = "library.settings"
#     _description = "Configurations"

#     _inherit = ['res.config.settings']

#     company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
#     days_before_reminder = fields.Integer(string='Days Before Reminder', related='company_id.days_before_reminder', readonly=False)
    
