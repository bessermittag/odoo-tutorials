# -*- coding: utf-8 -*-

from odoo import fields, models

class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property','user_id')
