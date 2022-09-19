from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(string="Patient", comodel_name='hospital.patient')
    gender = fields.Selection([('male', 'Male'), ('female', "Female")], string="Gender", related='patient_id.gender')
    patient_age = fields.Integer('Age', help="Patient Age")
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Highest')],
        'Priority', default='1')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        'Status', default='draft', required=True, )

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.patient_age = self.patient_id.patient_age

    def action_progress(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Clicked Successfully',
                'type': 'rainbow_man',
            }
        }
