import datetime
from odoo import models, fields, api, exceptions, _ 


class LibraryRental(models.Model):
    _name = "library.rental"
    _description = "Rental Information"

    _inherit = ['mail.thread', 'mail.activity.mixin']

    renting_member = fields.Many2one(comodel_name='res.partner', string='Member',required=True, ondelete='cascade', domain="[('is_member', '=', True)]")
    rented_book = fields.Many2one('library.book', string='Book')
    start_date = fields.Datetime(string='Rental Date')
    maxend_date = fields.Datetime(string='Return Before')
    end_date = fields.Datetime(string='Return Date')
    rental_state = fields.Selection([('available', 'Available'),('pending', 'Pending Return'), ('returned', 'Returned')], default='pending')
    genre = fields.Many2many(related='rented_book.genre_ids', string='Genre')
    
    @api.model
    def send_auto_reminder (self):
        today = fields.Date.today()
        reminder_date = today + timedelta(days=self.env.company.days_before_reminder)
        pending_rentals = self.search([('state', '=', 'pending'), ('maxend_date', '<=', reminder_date)])

        for rental in pending_rentals:
            template = self.env.ref('library.email_template_library_reminder')
            template.send_mail(library.rental.id, force_send=True)

    def action_send_manual_reminder(self):
        # template = self.env.ref('library.email_template_library_reminder')
        # return self.env['mail.compose.message']._action_send_mail(
        #     res_model='library.rental',
        #     res_id=self.ids,
        #     template_id=template.id,
        #     composition_mode='comment',
        # )

        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        ctx = {
            'default_model': 'library.rental',
            'default_res_ids': self.ids,
            'default_template_id': 'library.email_template_library_reminder',
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }





  
  
        # for rec_id in self._context["active_ids"]:
        #     ctx={}
        #     ctx['email_to']=#get the user email
        #     ctx['email_from']= self.env.user.work_email
        #     ctx['send_email']= True
        #     template = self.envref('library.email_template_library_reminder')
        #     template.with_context(ctx).send_mail(rec_id, force_send=True, raise_exception=False)

