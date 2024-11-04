from odoo import models, fields


class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _desription="Estate Property Type"
    _order = 'sequence desc'


    name = fields.Char(string="Property Type", required = True)
    sequence = fields.Integer (default = 1)
    property_ids = fields.One2many ("estate.property","estate_property_type_id")