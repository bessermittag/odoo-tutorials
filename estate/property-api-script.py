import xmlrpc.client

# Odoo API information: edit it to match your config
url = 'https://nextorderde-odoo-sh-main-staging-12538921.dev.odoo.com/'
db = 'nextorderde-odoo-sh-main-staging-12538921'
username = 'admin'
password = 'admin'
# password = 'api_key'  # alternative to password

# Connect to Odoo API
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# Retrieve any information (public methods only)
property1 = models.execute_kw(db, uid, password, 'estate.property', 'read', [[1]])
print(property1)

# models.execute_kw(db, uid, password, 'estate.property', 'search_read', [[], ["name", "description"]])
args = [[('expected_price', '>', 10000)]]
kwargs = {"fields": ["name", "description"]}
property_fields = models.execute_kw(db, uid, password, 'estate.property', 'search_read', args, kwargs)
print(property_fields)