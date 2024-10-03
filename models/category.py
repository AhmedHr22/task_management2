from odoo import api,fields,models
from odoo.exceptions import ValidationError


class Category(models.Model):
    _name="category.managements"
    _description = """category module """
    _rec_name = 'titled'

    titled = fields.Char(required=True,string="titled")

    # task2
    def action_open_tasks_by_category(self):
        return{
            'name':f'Tache de categorie {self.titled}',
            'type':'ir.actions.act_window',
            'res_model':'task.managements',
            'domain':[('category_id','=',self.titled)],
            'view_mode':'tree,form'
        }