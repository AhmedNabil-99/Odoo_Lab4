from odoo import models, fields

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Department'

    name = fields.Char(string='Department Name', required=True)
    capacity  = fields.Integer('Capacity')
    is_opened = fields.Boolean('Opened')
    # patients = fields.Char('Patients')

    patient_ids = fields.One2many('hms.patient', 'department_id')