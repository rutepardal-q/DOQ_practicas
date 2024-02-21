
from odoo import models, fields, api, _ 

class LibraryAuditMixing(models.AbstractModel):
    _name = 'library.audit.mixing'
    _description = 'Audit Abstract Model'

    
    # CREATE

    @api.model_create_multi
    def create(self, vals_list):   
        newrecs = super().create(vals_list)
        for newrec in newrecs:
            audit_values = {
                'user_id': self.env.user.id,
                'date': fields.Datetime.now(),
                'operation': 'create',
                'res_id': newrec.id,
                'res_mod': self._name,
                }
            self.env['library.audit'].create(audit_values)
        return newrecs
    
    # EDITS

    def write(self, values):     
        chrec = super(LibraryAuditMixing, self).write(values)
        audit_values = {
            'user_id': self.env.user.id,
            'date': fields.Datetime.now(),
            'operation': 'write',
            'res_id': chrec.id,
            'res_mod': self._name,
        }
        self.env['library.audit'].create(audit_values)

        return chrec
    
        # DELETING
    
    def unlink(self):
        delrec = super(LibraryAuditMixing, self).unlink()
        audit_values = {
            'user_id': self.env.user.id,
            'date': fields.Datetime.now(),
            'operation': 'unlink',
            'res_id': delrec.id,
            'res_mod': self._name,
        }
        self.env['library.audit'].create(audit_values)

        return delrec