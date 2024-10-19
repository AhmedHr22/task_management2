from odoo import api,fields,models

class AllTaskDetailsReport(models.AbstractModel):
    _name="report.task_management_2.report_task_details_template"
    _description="report all task from wizard"


    @api.model
    def _get_report_values(self,docids,data=None):
        docs = self.env['task.managements'].search([])
        import logging
        logging.info(f'\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> info >>>>>>>>>>>>>>>>>>>>>>docs : {docs} \n\n')

        return {
            "docs" : docs
        
        }