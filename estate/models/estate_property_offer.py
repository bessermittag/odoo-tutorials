# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(string='Validity (days)')
    date_deadline = fields.Date(string="Deadline", computed='_compute_date_deadline', inverse='_inverse_date_deadline')


    @api.onchange('validity')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = fields.Date.add(fields.Date.today(), days=rec.validity)

    @api.onchange('date_deadline')
    def _inverse_date_deadline(self):
        for rec in self:
            create_date = rec.create_date if rec.create_date else fields.Date.today()
            rec.validity = (rec.date_deadline - fields.Date.today()).days
