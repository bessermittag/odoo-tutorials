# -*- coding: utf-8 -*-
from xml.dom import ValidationErr
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero
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
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    property_tag_id = fields.Many2many("estate.property.tag", string="Property Tags")
    property_offers = fields.One2many("estate.property.offer","property_id")

    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(string='Best Offer', readonly=True,compute='_compute_best_price', store=True)
    offer = fields.One2many("estate.property.offer","property_id")

    @api.depends("offer.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(self.offer.mapped('price')) if record.offer else 0

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
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("Canceled Properties can not be sold."))
            record.state = 'sold'
        return True

    @api.depends('property_offers.status')
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold Properties can not be canceled."))
            record.state = 'canceled'
        return True
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0 )',
         'The expected price must be strictly positive.'),
         ('check_selling_price', 'CHECK(selling_price >= 0 )',
         'selling price must be positive.')

        ]
    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):

         if not (float_is_zero(self.expected_price) or float_compare(self.selling_price, self.expected_price * 0.9, precision_rounding=self.company_id.currency_id.rounding)):
            raise ValidationErr("Selling price cannot be lower than 90% of the expected price!")

    