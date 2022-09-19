from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'patient_name'
    _description = 'Patient Record'

    patient_name = fields.Char(string='Patient Name', required=True, tracking=True)
    patient_age = fields.Integer('Age')
    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Image')
    gender = fields.Selection([('male', 'Male'), ('female', "Female")], string="Gender", default='male')
    name_sec = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one(string="Appointments", comodel_name='hospital.appointment')

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name_sec', _('New')) == _('New'):
            vals['name_sec'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')

        result = super(HospitalPatient, self).create(vals)
        return result
