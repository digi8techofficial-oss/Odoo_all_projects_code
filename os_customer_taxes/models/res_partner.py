from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    other_tax_ids = fields.Many2many(
        'account.tax',
        string='Extra Taxes',
        help="These taxes will be automatically added to invoice lines for this customer."
    )
