from odoo import models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('product_id', 'product_uom_id', 'partner_id')
    def _compute_tax_ids(self):
        # Let Odoo compute the default product taxes first
        super()._compute_tax_ids()
        
        for line in self:
            # Check if there is a partner on the move (Invoice Customer)
            partner = line.move_id.partner_id
            if not partner and line.partner_id:
                partner = line.partner_id
                
            if partner and partner.other_tax_ids:
                # Add the partner's extra taxes to the existing taxes
                # The | operator handles the set union, ensuring no duplicates
                current_taxes = line.tax_ids
                extra_taxes = partner.other_tax_ids
                
                # Filter taxes by company to be safe, though usually handled by domain
                if line.company_id:
                    extra_taxes = extra_taxes.filtered(lambda t: t.company_id == line.company_id)
                
                line.tax_ids = current_taxes | extra_taxes
