import xmlrpc.client

# Odoo API information: edit it to match your config
url = 'https://nextorderde-odoo-sh-main-staging-12538921.dev.odoo.com/'
db = 'nextorderde-odoo-sh-main-staging-12538921'
api_key = 'api_key'
# password = 'api_key '  # alternative to password

# Connect to Odoo API
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, api_key, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Retrieve any information (public methods only)
