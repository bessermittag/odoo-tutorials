# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class PropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline',)

    _sql_constraints = [
        ('price_check', 'CHECK(price >0)', 'The price must be positive!'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = fields.Date.add(fields.Date.today(), days=rec.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for rec in self:
            create_date = rec.create_date if rec.create_date else fields.Date.today()
            rec.validity = (rec.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['sold', 'canceled']:
                raise UserError(_('Offers for canceled or sold Properties can\'t be accepted.'))
            elif record.property_id.state == 'offer_accepted':
                raise UserError(_('There is already an accepted Offer for this Property.'))
            record.status = 'accepted'
            record.property_id.write({
                'state': 'offer_accepted',
                'partner_id': record.partner_id,
                'selling_price': record.price,
            })
            (record.property_id.property_offers - record).status = 'refused'
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.state in ['sold', 'canceled']:
                raise UserError(_('Offers for canceled or sold Properties can\'t be refused.'))
            if record.status == 'accepted':
                record.property_id.write({
                    'partner_id': False,
                    'selling_price': False,
                    'state': 'new',
                })
            record.status = 'refused'
        return True

