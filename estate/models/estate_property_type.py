# -*- coding: utf-8 -*-
from odoo import fields, models

class PropertyTypeModel(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type Model'

    name = fields.Char(required=True)
