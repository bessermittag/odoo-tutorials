from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'  # This defines the model name

    name = fields.Char(string="Property Type", required=True)
    description = fields.Text(string="Estate Property Type Model")