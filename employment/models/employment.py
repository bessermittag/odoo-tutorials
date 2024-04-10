# -*- coding: utf-8 -*-
from odoo import fields, models

class EmploymentModel(models.Model):
    _name = 'employment'
    _description = 'Employment Model'

    partner_id = fields.Many2one('res.partner', string='Employee (Customer)', copy=False, domain=[('is_company', '=', False)])
    company_partner_id = fields.Many2one('res.partner', string='Employer (Company)', copy=False, domain=[('is_company', '=', True)])
    email = fields.Char()
    employee_id = fields.Char(string='Employee ID')
    state = fields.Selection(
        string='Status',
        selection=[('pending','Pending'),('confirmed','Confirmed'),('revoked','Revoked')],
        required=True,
        copy=False,
        default='pending'
    )
    active = fields.Boolean(default=True)
