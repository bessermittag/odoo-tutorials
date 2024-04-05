# -*- coding: utf-8 -*-
from odoo import fields, models

class PropertyTagModel(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag Model'

    name = fields.Char(required=True)
    _sql_constraints = [
        ('estate_property_tag', 'UNIQUE(name)','Property Tag name must be unique')
    ]
