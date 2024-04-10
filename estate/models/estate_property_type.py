# -*- coding: utf-8 -*-
from odoo import fields, models, api

class PropertyTypeModel(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type Model'
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence')
    property_ids = fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many('estate.property.offer','property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')
    _sql_constraints = [
        ('estate_property_type', 'UNIQUE(name)','Property Type name must be unique')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
