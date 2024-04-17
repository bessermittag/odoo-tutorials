# -*- coding: utf-8 -*-
from odoo import fields, models

class PropertyTagModel(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag Model'
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
    _sql_constraints = [
        ('estate_property_tag', 'UNIQUE(name)','Property Tag name must be unique')
    ]
