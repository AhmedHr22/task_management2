from odoo import api,fields,models
from odoo.exceptions import ValidationError

class ConfirmationWizard(models.TransientModel):
    _name="task.confirmation.wizard"

    category_id = fields.Many2one("category.managements",string="Categorie")
    delay = fields.Boolean(string="En retard",)
    state = fields.Selection([
        ('broullion','Broullion'),
        ('en_cour','En cour'),
        ('terminer','Terminer')],
        string="State")
    due_date_start = fields.Date(string="Date echeance debut")
    due_date_end = fields.Date(string="Date echeance fin")

    def action_print_report(self):
        data = {
            "form_data" : self.read()[0]
        }
        return self.env.ref('task_management_2.action_report_all_task_details').report_action(self,data=data)

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     report = self.env['ir.actions.report']._get_report_from_name('account_test.report_accounttest')
    #     records = self.env['accounting.assert.test'].browse(self.ids)
    #     return {
    #         'doc_ids': self._ids,
    #         'doc_model': report.model,
    #         'docs': records,
    #         'data': data,
    #         'execute_code': self.execute_code,
    #         'datetime': datetime
    #     }