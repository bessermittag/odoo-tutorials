# -*- coding: utf-8 -*-
from odoo import fields, models
import random

class PropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=lambda self: self._get_default_color())

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The Tag name has to be unique!'),
    ]

    def _get_default_color(self):
        return random.randint(1,11)