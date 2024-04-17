# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from passlib.context import CryptContext
class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property','user_id')
  # API keys support
API_KEY_SIZE = 20 # in bytes
INDEX_SIZE = 8 # in hex digits, so 4 bytes, or 20% of the key
KEY_CRYPT_CONTEXT = CryptContext(
    # default is 29000 rounds which is 25~50ms, which is probably unnecessary
    # given in this case all the keys are completely random data: dictionary
    # attacks on API keys isn't much of a concern
    ['pbkdf2_sha512'], pbkdf2_sha512__rounds=6000,
)
class ApiKey(models.Model):
    _inherit = 'res.users.apikeys'

    expiration_date = fields.Datetime(string="Expiration Date",required=True)
    
    def _check_credentials(self, *, scope, key):
        assert scope, "scope is required"
        index = key[:INDEX_SIZE]
        self.env.cr.execute('''
            SELECT user_id, key
            FROM {} INNER JOIN res_users u ON (u.id = user_id)
            WHERE u.active and index = %s AND (scope IS NULL OR scope = %s) AND (expiration_date > CURRENT_TIMESTAMP)
        '''.format(self._table),
        [index, scope])
        for user_id, current_key in self.env.cr.fetchall():
            if KEY_CRYPT_CONTEXT.verify(key, current_key):
                return super()._check_credentials(scope)
      