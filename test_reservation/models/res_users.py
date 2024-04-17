from odoo import api, fields, models, Command


class ResUsers(models.Model):
    _inherit = 'res.users'

    main_order_id = fields.Many2one(
        'sale.order',
    )

    _sql_constraints = [
        ('main_order_id_uniq', 'unique(main_order_id)', 'A user\'s main order is his own.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        users._create_main_order()
        return users

    def _create_main_order(self):
        for user in self:
            user.main_order_id = self.env['sale.order'].create({
                'user_id': user.id,
                'partner_id': user.partner_id.id,
                'order_line': [Command.create({
                    'name': 'EXPIRED RESERVATIONS',
                    'display_type': 'line_section',
                })]
            })
        user.mapped('main_order_id').action_confirm()

    def get_reservations(self):
        self.ensure_one()
        if not self.main_order_id:
            self._create_main_order()
        self.main_order_id._clear_old_reservations()
        return self.main_order_id.order_line.filtered(lambda sol: not sol.display_type and sol.product_uom_qty > 0)

    @api.model
    def _action_create_invoices_for_main_so(self):
        users = self.search([('main_order_id', '!=', False)])
        users = users.with_context(raise_if_nothing_to_invoice=False)
        moves = users.mapped('main_order_id')._create_invoices()
