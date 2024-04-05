# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PropertyOfferModel(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer Model'

    price = fields.Float()
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(string='Validity (days)',default=7)
    date_deadline = fields.Date(string='Deadline',compute='_compute_date_deadline',inverse='_inverse_date_deadline')
    _sql_constraints = [
        ('estate_property_offer_check_price', 'CHECK(price > 0)','Property Offer Price must be strictly positive')
    ]

    @api.depends('validity','date_deadline')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Datetime.today()
            record.date_deadline = fields.Date.add(create_date.date(), day=record.validity)

    @api.depends('validity','date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Datetime.today()
            record.validity = (record.date_deadline - create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state in ['sold','canceled']:
                raise UserError(_('Offers for canceled or sold Properties can\'t be accepted.'))
            elif record.property_id.state == 'offer_accepted':
                raise UserError(_('There is already an accepted Offer for this Property.'))
            record.status = 'accepted'
            record.property_id.write({
                'state': 'offer_accepted',
                'partner_id': record.partner_id,
                'selling_price': record.price,
            })
            (record.property_id.offer_ids - record).status = 'refused'
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.property_id.state in ['sold','canceled']:
                raise UserError(_('Offers for canceled or sold Properties can\'t be refused.'))
            if record.status == 'accepted':
                record.property_id.write({
                    'partner_id': False,
                    'selling_price': False,
                    'state': 'new',
                })
            record.status = 'refused'
        return True
