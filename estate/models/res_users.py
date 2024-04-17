# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from passlib.context import CryptContext
class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property','user_id')
        