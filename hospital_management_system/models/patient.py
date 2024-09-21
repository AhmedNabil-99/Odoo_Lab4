from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required =True)
    last_name = fields.Char(string='Last Name', required =True)
    birth_date = fields.Date(string='Birth Date', required =True)
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([('a', 'A'),
                                   ('b', 'B'),
                                   ('ab', 'AB'),
                                   ('o', 'O')])
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address', required =True)
    age = fields.Integer(string='Age', required =True)
    email = fields.Char()

    # relations
    department_id = fields.Many2one('hms.department')
    doctor_ids = fields.Many2many('hms.doctor')
    log_history = fields.One2many('hms.patient.log', 'patient_id')


    # department_capacity = fields.Integer(related='department_id.capacity')
    remaining_capacity = fields.Integer(string='Remaining Department Capacity', compute='_compute_remaining_capacity')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined', string='state')

    def action_undetermined(self):
        self.write({'state': 'undetermined'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Undetermined'
        })

    def action_good(self):
        self.write({'state': 'good'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Good'
        })

    def action_fair(self):
        self.write({'state': 'fair'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Fair'
        })

    def action_serious(self):
        self.write({'state': 'serious'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Serious'
        })

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio_required(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

    @api.onchange('age')
    def onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
        if self.age < 50:
            self.history = False

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age = 0

    @api.depends('department_id')
    def _compute_remaining_capacity(self):
        for record in self:
            if record.department_id:
                total_capacity = record.department_id.capacity
                assigned_patients = len(record.department_id.patient_ids)
                record.remaining_capacity = total_capacity - assigned_patients
            else:
                record.remaining_capacity = 0

    @api.constrains('email')
    def _check_email_validity(self):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for rec in self:
            if rec.email and not re.match(email_regex, rec.email):
                raise ValidationError('Please enter a valid email address.')

    _sql_constraints = [
        ('unique_email', 'unique(email)', 'The email address must be unique.')
    ]


class PatientLog(models.Model):
        _name = 'hms.patient.log'
        _description = 'Patient Log'

        patient_id = fields.Many2one('hms.patient')
        date = fields.Datetime(default=fields.Datetime.now)
        description = fields.Text()


