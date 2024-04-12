from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _create_main_order(self):
        if not self.id or isinstance(self.id, models.NewId):
            return False
        return self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
        })

    main_order_id = fields.Many2one(
        'sale.order',
        default=_create_main_order,
    )

    _sql_constraints = [
        ('main_order_id_uniq', 'unique(main_order_id)', 'A user\'s main order is his own.'),
    ]

    def get_reservations(self):
        self.ensure_one()
        return self.main_order_id.order_line.filtered(lambda sol: sol.quantity > 0)
