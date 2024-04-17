from odoo import fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"

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
        pickings = self.picking_ids

        for line in order_lines:
            print(line.product_uom_qty - line.qty_delivered)
        print(pickings)
        for picking in pickings:
            moves = picking.move_ids
            print(moves)
            for move in moves:
                move_lines = move.move_line_ids
                print(move_lines)
                for ml in move_lines:
                    print(ml.product_id)
                    print(ml.quantity)
        raise UserError(_("Test."))
