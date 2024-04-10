# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    employee_ids = fields.One2many('employment','company_partner_id')
    company_ids = fields.One2many('employment','partner_id')
