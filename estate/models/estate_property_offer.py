# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(string='Validity (days)',default=7)
    date_deadline = fields.Date(string='Deadline',compute='_compute_date_deadline',inverse='_inverse_date_deadline')

    @api.depends("validity","date_deadline")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, day=record.validity)

    @api.depends("validity","date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.validity = (create_date - record.date_deadline).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state in ['sold','canceled']:
                raise UserError(_("Offers for canceled or sold Properties can't be accepted."))
            elif record.property_id.state == 'offer_accepted':
                raise UserError(_("There is already an accepted Offer for this Property."))
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price
            for other_offer in record.property_id.offer_ids:
                if other_offer.id != record.id:
                    other_offer.status = 'refused'
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.property_id.state in ['sold','canceled']:
                raise UserError(_("Offers for canceled or sold Properties can't be refused."))
            if record.status == 'accpeted':
                record.property_id.partner_id = False
                record.property_id.selling_price = False
                record.property_id.state = 'new'
            record.status = 'refused'
        return True
