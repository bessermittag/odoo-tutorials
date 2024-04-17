from odoo import api, fields, models, Command,exceptions
from datetime import timedelta
import binascii
import os

from odoo.odoo.addons.base.models.res_users import KEY_CRYPT_CONTEXT
from odoo.odoo.http import request, _logger

API_KEY_SIZE = 20
INDEX_SIZE = 8


class ResUsers(models.Model):
    _inherit = 'res.users'

    main_order_id = fields.Many2one(
        'sale.order',
    )

    _sql_constraints = [
        ('main_order_id_uniq', 'unique(main_order_id)', 'A user\'s main order is his own.'),
    ]

    api_key_expiration_date = fields.Datetime(string='API Key Expiration Date')

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        users._create_main_order()
        return users

    def _create_main_order(self):
        for user in self:
            user.main_order_id = self.env['sale.order'].create({
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



class APIKeys(models.Model):
    _inherit = 'res.users.apikeys'

    expiration_date = fields.Datetime(string='Expiration Date', required=False, default= fields.Datetime.now() + timedelta(days=30))
    #TODO: Add functionality to set expiration date when creating API key
    #TODO: Add functionalty to expand expiration date for a user
    #TODO: Add functionality to check expiration date for a user
    #TODO: set default expiration date to 30 days


    def _generate(self, scope, name, expiration_date=None):
        k = binascii.hexlify(os.urandom(API_KEY_SIZE)).decode()
        # store the ex_date in the database
        self.env.cr.execute("""
        INSERT INTO {table} (name, user_id, scope, key, index, expiration_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """.format(table=self._table),
        [name, self.env.user.id, scope, KEY_CRYPT_CONTEXT.hash(k), k[:INDEX_SIZE], expiration_date])

        ip = request.httprequest.environ['REMOTE_ADDR'] if request else 'n/a'
        _logger.info("%s generated: scope: <%s> for '%s' (#%s) from %s",
            self._description, scope, self.env.user.login, self.env.uid, ip)

        return k

    def _check_credentials(self, *, scope, key):

        now = fields.Datetime.now()
        self.env.cr.execute('''
               SELECT  key
               FROM {} 
               WHERE (active AND expiration_date < %s)
           '''.format(self._table),
                            [fields.Datetime.now()])
        keys = self.env.cr.fetchall()
        keys.active = False
        keys.scope = 'Expired on {}'.format(now)
        keys.flush_recordset('active', 'scope')
        return super()._check_credentials(scope=scope, key=key)

#add a new scope for a new type of user( e.g scope =4 user-specific) and specify the expiration date for type of the scope

