from odoo import api,fields,models
from odoo.exceptions import ValidationError

class Task(models.Model):
    _name="task.managements"
    _description = """
    a module for task management
    """

    title = fields.Char(required=True,string="Titre")
    description = fields.Text(required=True,string="Description")
    due_date = fields.Date(required=True,string="Date Echeance") 
   
    delay = fields.Boolean(string="Retard")
    priority = fields.Selection(
        [('basse','Basse'),
         ('moyenne','Moyenne'),
         ('haute','Haute')],
         default="basse",
         required=True,
         string="Priorite")
   
    patern = fields.Char(required=True,string='Motif')
    state = fields.Selection(
        [('broullion','Broullion'),
         ('en_cour','En cours'),
         ('terminer','Terminer')],
         default='broullion',
         required=True,
         string="State")
    
    category_id = fields.Many2one('category.managements',string="Categorie",required=True)
    

    def start(self):
        for rec in self:
            rec.state = "en_cour"
    
    def in_draft(self):
        for rec in self:
            rec.state = "broullion"

    def conclude(self):
        for rec in self:
            rec.state = "terminer"

    def unlink(self):
        for rec in self:
            if rec.state != "broullion":
                raise ValidationError("pour supprimer une tache il fau que l etat soit en broullion")
            
        return super(Task,self).unlink()
    












