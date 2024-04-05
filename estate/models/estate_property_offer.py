# -*- coding: utf-8 -*-
from . import models, fields

class PropertyOfferModel(models.model)
   _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

   price = fields.Float(required=True)
    status = fields.Selection(
         string='Status',
         selection=[('accepted','Accepted'),('refused','Refused')],
         copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Buyer')
    property_id = fields.Many2one('estate.property', string='Property')


