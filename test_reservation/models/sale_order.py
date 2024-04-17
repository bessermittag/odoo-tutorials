import math
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta



class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.constrains("user_id")
    def _check_user_id_matches_main_order_id(self):
        for order in self.filtered(lambda o: o.user_id.main_order_id):
            if order.user_id.main_order_id != order:
                raise ValidationError(_("If a user has a main order, that order must be assigned to that user."))
            if order.user_id.partner_id != order.partner_id:
                raise ValidationError(_("If a user has a main order, that order must be directed to the related partner."))

    def _clear_old_reservations(self):
        old_lines = self.mapped("order_line").filtered(
            lambda sol: not sol.display_type and sol.create_date < fields.Datetime.now() - timedelta(minutes=10)
        )
        old_lines.product_uom_qty = 0
        for line in old_lines:
            section_seq = line.order_id.order_line.filtered(
                lambda sol: sol.display_type == "line_section" and sol.name == "EXPIRED RESERVATIONS"
            )
            if section_seq:
                line.sequence = section_seq.sequence + 1

    def action_pickup_half(self):
        order_lines = self.mapped("order_line")
        for picking in self.picking_ids:
            for move in picking.move_ids:
                for ml in move.move_line_ids:
                    if (ml.quantity > 0):
                        ml.write({
                            'quantity': math.ceil(ml.quantity / 2)
                        })
            picking.picking_type_id.create_backorder = 'always'
            picking.button_validate()
        raise UserError(_("Test."))
