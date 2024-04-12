# -*- coding: utf-8 -*-
from odoo import models, Command

class PropertyModel(models.Model):
    _inherit = 'estate.property'

    def action_update_state_sold(self):
        self.ensure_one()
        self.env['account.move'].create(
            {
                'partner_id': self.partner_id.id,
                'move_type' : 'out_invoice',
                'invoice_line_ids': [
                    Command.create(
                        {
                            'name': self.name,
                            'quantity': 1,
                            'price_unit': self.selling_price * 0.06
                        }
                    ),
                    Command.create(
                        {
                            'name':'Administrative Fee',
                            'quantity': 1,
                            'price_unit': 100
                        }
                    ),
                ],
            }
        )
        return super().action_update_state_sold()
