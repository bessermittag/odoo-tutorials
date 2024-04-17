# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.base.models.res_users import API_KEY_SIZE, INDEX_SIZE, KEY_CRYPT_CONTEXT
from passlib.context import CryptContext
class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property','user_id')

class ApiKeys(models.Model):
    _inherit = 'res.users.apikeys'

    # expiration_date = fields.Datetime(
    #     string="Expiration Date",
    #     required=True,
    #     default=fields.Datetime.add(fields.Datetime.today(), months=3)
    # )
    # Adding a field required extending the _generate method
    # (may run into issues if field is required)
    # def _generate(self, ...):
    #     k = super()._generate(...)
    #     index = k[:INDEX_SIZE]
    #     find row with matching index
    #     insert expiration_date into row

    def _check_credentials(self, *, scope, key):
        """
        Before checking the credentials, update the expiration date of the key.
        """
        now = fields.datetime.now()
        # Update WHERE clause to only "expire" keys for API users (not EVERY api key)
        self.env.cr.execute('''
            SELECT id
            FROM {}
            WHERE (create_date + INTERVAL '10 minute' < %s)
        '''.format(self._table),
        [now]) # fields.Datetime.to_string
        key_ids = self.env.cr.fetchall()
        keys = self.browse(key_ids)
        keys.sudo().scope = 'Expired on {}'.format(now)
        keys.flush_recordset(['scope'])

        return super()._check_credentials(scope=scope, key=key)
