from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    show_company_logo_fbr = fields.Boolean(string="Show Company Logo in FBR Report", default=True)
