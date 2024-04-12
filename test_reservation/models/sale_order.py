from odoo import fields, models
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
