# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    name = fields.Char(string='Title', required=True)
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
    garden_area = fields.Integer(string='Garden Area (sqm)', default=10)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        default='north'
    )
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    state = fields.Selection(
        string='Status',
        selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
        required=True,
        copy=False,
        default="new"
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    property_tag_id = fields.Many2many("estate.property.tag", string="Property Tags")
    property_offers = fields.One2many("estate.property.offer","property_id")
    best_price = fields.Float(string="Best Offer", readonly=True, compute='_compute_best_price', store=True)


    @api.onchange('living_area','garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('property_offers.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.property_offers.mapped('price')) if rec.property_offers else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False



    @api.depends('property_offers.status')
    def action_sold(self):
        if self.state == 'canceled':
            raise UserError(_("You cannot set a canceled property as sold."))
        self.state = 'sold'

    @api.depends('property_offers.status')
    def action_cancel(self):
        if self.state == 'sold':
            raise UserError(_("You cannot cancel a sold property."))
        self.state = 'canceled'

