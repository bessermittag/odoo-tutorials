# -*- coding: utf-8 -*-

from odoo import models, fields, api , _, Command

class EstatePropertyInherit(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
      self.env['account.move'].create({
          'partner_id': self.partner_id.id,
          'move_type': 'out_invoice',
          'invoice_date': fields.Date.today(),
          'invoice_line_ids': [
              Command.create({
                'name': 'Property Sale',
                'quantity': 1,
                'price_unit': self.selling_price * 0.06,
            }),
              Command.create({
                'name': 'Administrative Fees',
                'quantity': 1,
                'price_unit': 100.00,
            })
          ]
        })
      return super(EstatePropertyInherit, self).action_sold()
