from odoo import api,fields,models
from odoo.exceptions import ValidationError
from datetime import datetime

class Task(models.Model):
    _name="task.managements"
    _description = """
    a module for task management
    """

    title = fields.Char(required=True,string="Titre")
    description = fields.Text(required=True,string="Description")
    due_date = fields.Date(required=True,string="Date Echeance") 
    delay = fields.Boolean(string="Retard",compute='compute_delay')
    priority = fields.Selection(
        [('basse','Basse'),
         ('moyenne','Moyenne'),
         ('haute','Haute')],
         default="basse",
         required=True,
         string="Priorite")
    patern = fields.Char(string='Motif')
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
                raise ValidationError("Pour supprimer une tache il faut que l'etat soit en broullion")
            
        return super(Task,self).unlink()
    
    @api.depends('due_date')
    def compute_delay(self):
            for rec in self:
                if rec.due_date:
                    rec.delay = datetime.today().date() > rec.due_date
                else:
                    rec.delay = False
    # task2
    user_id = fields.Many2one('res.users',string="Utilisateur",default=lambda self:self.env.user)

    









