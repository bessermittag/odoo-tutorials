# -*- coding: utf-8 -*-
from odoo import fields, models

class PropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The Tag name has to be unique!'),
    ]