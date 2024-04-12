# -*- coding: utf-8 -*-
from odoo import models, Command

class PropertyModel(models.Model):
    _inherit = 'estate.property'

    def action_update_state_sold(self):
        move_lines = []
        move_lines.append(Command.create({
            'name': self.name,
            'quantity': 1,
            'price_unit': self.selling_price * 0.06
        }))
        move_lines.append(Command.create({
            'name':'Administrative Fee',
            'quantity': 1,
            'price_unit': 100
        }))
        move_vals = {
                'partner_id': self.partner_id.id,
                'move_type' : 'out_invoice',
                'invoice_line_ids': move_lines,
            }
        self.env['account.move'].create(move_vals)
        return super().action_update_state_sold()
