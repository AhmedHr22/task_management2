from odoo import api,fields,models
from odoo.exceptions import ValidationError
from datetime import datetime

class Task(models.Model):
    _name="task.managements"
    _description = """
    a module for task management
    """
    _rec_name = "title"

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
    # task4
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

    # task4
    is_category_travail = fields.Boolean(default=False,compute="compute_category_id")
    @api.depends("category_id")
    def compute_category_id(self):
        category_travail = self.env.ref('task_management_2.category_record')
        for rec in self:
            import logging
            logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>category_id {rec.category_id} \n\n')
            logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>category_travail {category_travail} \n\n')

            rec.is_category_travail = category_travail == rec.category_id
            
    linked_task = fields.Many2one('task.managements',string="Tache depandante")
    @api.constrains('linked_task')
    def check_linked_task(self):
        import logging
        logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>linked_task_state {self.linked_task.state} \n\n')
        logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>state {self.state} \n\n')

        if self.linked_task.state == "terminer" and self.state == "broullion" :
            self.start()  
        elif not self.linked_task:
            import logging
            logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>linked task_null : {self.linked_task} \n\n')
        else:    
            raise ValidationError("la tache depandante elle doit etre terminer pour commencer la tache courante")


    # tache5
    attachement = fields.Many2many('ir.attachment',string="Piece jointe")










