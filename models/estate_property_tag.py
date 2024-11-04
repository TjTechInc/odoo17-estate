from odoo import models , fields

class EstateTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Tags"
    _sql_constrains = [
        ("unique_tag_name", "UNIQUE(name)","Tag names should be unique")
    ]
    _order = ' name desc'

    name = fields.Char("Property Tag")
    color = fields.Integer(string='Color Index')
    