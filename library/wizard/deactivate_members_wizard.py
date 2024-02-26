from odoo import models, fields, api, _


class DeactivateMembersWizard(models.TransientModel):
    _name ='library.deactivate.members.wizard'
    _description = 'Deactivate Member Files'

    motive_deact = fields.Text (string='Deactivation Motive', required=True)
    

    # Deactivate Members
        
    def action_confirm_deact_button(self):
        """ Saves Deactivate motive to chatter """
        member_id=self.env.context.get('active_id')
        member = self.env['res.partner'].browse(member_id)
        

        member.write({
            'is_member': False,
        })

        member.message_post(body=f"Deactivation Motive: {self.motive_deact}")

        return {'type': 'ir.actions.act_window_close'}
