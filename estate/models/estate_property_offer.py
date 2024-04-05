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
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline',)

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
        accepted_offers = self.env['estate.property.offer'].search(
            [('property_id', '=', self.property_id.id), ('status', '=', 'accepted')])
        if accepted_offers:
            raise UserError(_("Only one offer can be accepted for a given property!"))

        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id.id

    def action_refuse(self):
        if self.property_id.state =='sold':
            raise UserError(_("You cannot refuse an offer for a sold property!"))
        self.status = 'refused'
        self.property_id.state = 'canceled'