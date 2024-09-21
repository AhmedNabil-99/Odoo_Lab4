from odoo import fields, models


class AddNewLog(models.TransientModel):
    _name = "hms.add.new.log"

    description = fields.Text('Log Description', required=True)
    patient_id = fields.Many2one('hms.patient', string="Patient", required=True)

    def add_new_log(self):
        self.env['hms.log.history'].create({
            'patient_id': self.patient_id.id,
            'description': self.description
        })