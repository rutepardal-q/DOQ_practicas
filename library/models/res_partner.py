from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_author = fields.Boolean(string="Author", default=False )
    is_member = fields.Boolean(string="Member", default=False )
    member_id = fields.Char(string="Member Number")
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    genre_ids = fields.Many2many(comodel_name='library.genre', string="Genres")

    @api.onchange('first_name', 'last_name')
    def _compute_full_name(self):
        self.name = ''
        if self.first_name:
            self.name += self.first_name
        if self.last_name:
            self.name += ' ' + self.last_name
    