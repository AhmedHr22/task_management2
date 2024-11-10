from odoo import api,fields,models
from odoo.exceptions import ValidationError
from datetime import datetime
import logging

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
            rec.is_category_travail = category_travail == rec.category_id
            
    linked_task = fields.Many2one('task.managements',string="Tache depandante")
    
    @api.constrains('linked_task')
    def check_linked_task(self):
        if self.linked_task.state == "terminer" and self.state == "broullion" :
            self.start()  
        elif not self.linked_task:
            import logging
            logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>linked task_null : {self.linked_task} \n\n')
        else:    
            raise ValidationError("la tache depandante elle doit etre terminer pour commencer la tache courante")


    # task5
    attachement = fields.Many2many('ir.attachment',string="Piece jointe")


    # task7
    number_sequence = fields.Char(string="Numero")
   
    def generate_sequence(self):
        # logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>searched seq : aaaa \n\n')
        current_user_id = self.env.user.id
        code_sequence = f"task_sequence{current_user_id}"
        seq = self.env['ir.sequence'].sudo().search([('code','=',code_sequence),('create_uid','=',current_user_id)],limit=1)
        # logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>searched seq : aaaa \n\n')
        logging.info(f"""\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>> searched seq :{seq} 
                     \n\n self.env.user : {current_user_id}
                     \n\n self.user_id : {self.user_id}  
                     \n\n self.create_uid : {self.create_uid} 
                     \n\n seq.create_uid : {seq.create_uid}
            """)

        if seq:
            return seq.next_by_code(code_sequence)
        else:
            vals = {
                "name":"task",
                "code":code_sequence,
                "prefix":"T",
                "padding":8,
                "implementation":"standard",
            }
            seq = self.env['ir.sequence'].sudo().create(vals)
            seq_var = seq.next_by_code(code_sequence)
            logging.info(f"""\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>> searched seq2 :{seq} 
                        \n\n self.env.user2 : {current_user_id}
                        \n\n self.user_id2 : {self.user_id}  
                        \n\n self.create_uid2 : {self.create_uid} 
                        \n\n seq.create_uid2 : {seq.create_uid}
                """)

            return seq_var
        

    @api.model
    def create(self,vals):
        vals["number_sequence"]= self.generate_sequence()
        logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>number_sequence : {vals} \n\n')
        
        res = super(Task,self).create(vals)
        logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>vals : {vals} \n\n')
        return res
    







