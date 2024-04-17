# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

class PropertyModel(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Model'
    _order = "id desc"

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
        default='new'
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer','property_id')
    total_area = fields.Float(string='Total Area (sqm)',compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer',compute='_compute_best_price')
    _sql_constraints = [
        ('estate_property_check_expected_price', 'CHECK(expected_price > 0)','Property Expected Price must be strictly positive'),
        ('estate_property_check_selling_price', 'CHECK(selling_price >= 0)','Property Selling Price must be positive')
    ]

    @api.constrains('expected_price','selling_price')
    def _check_selling_price(self):
        for record in self:
            precision = self.env.company.currency_id.decimal_places
            if float_compare(record.selling_price, 0, precision) == 1 and float_compare(record.selling_price, record.expected_price * 0.9, precision) == -1:
                raise ValidationError('The Selling Price must be at least 90% of the Expected Price! You must reduce the Expected Price if you want to accept this Offer.')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(self.offer_ids.mapped('price') + [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.write({
                'garden_area': 10,
                'garden_orientation': 'north',
            })
        else:
            self.write({
                'garden_area': 0,
                'garden_orientation': False,
            })

    def action_update_state_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_('Canceled Properties can not be sold.'))
            record.state = 'sold'
        return True

    def action_update_state_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Sold Properties can not be canceled.'))
            record.state = 'canceled'
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_or_canceled(self):
        if any(record.state not in ['new','canceled'] for record in self):
            raise UserError(_("Only new and canceled Properties can be deleted."))
