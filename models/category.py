from odoo import api,fields,models
from odoo.exceptions import ValidationError


class Category(models.Model):
    _name="category.managements"
    _description = """category module """
    _rec_name = 'titled'

    titled = fields.Char(required=True,string="titled")