# -*- coding: utf-8 -*-
from odoo import fields, models

class PropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    name = fields.Char(string='Title',required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From',
        copy=False,
        default=fields.Datetime.add(fields.Datetime.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'),('south','South'),('east','East'),('west','West')]
    )
    state = fields.Selection(
        string='Status',
        selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
        required=True,
        copy=False,
        default="new"
    )
    active = fields.Boolean(default=True)
