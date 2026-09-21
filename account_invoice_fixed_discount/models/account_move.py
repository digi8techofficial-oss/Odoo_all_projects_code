from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class AccountMove(models.Model):
    _inherit = "account.move"

    total_discount = fields.Monetary(
        string="Total Discount",
        currency_field="currency_id",
        compute="_compute_total_discount",
        store=True,
        help="Total discount (both fixed and percentage-based) applied on all invoice lines.",
    )

    @api.depends("invoice_line_ids.price_unit", "invoice_line_ids.discount", "invoice_line_ids.discount_fixed", "invoice_line_ids.quantity")
    def _compute_total_discount(self):
        """Compute total discount from all invoice lines (including fixed discount logic)."""
        for move in self:
            total_discount = 0.0
            currency = move.currency_id or move.company_id.currency_id

            for line in move.invoice_line_ids:
                # Case 1: If fixed discount is applied
                if line.discount_fixed:
                    total_discount += line.discount_fixed * line.quantity
                # Case 2: If percentage discount is applied
                elif line.discount:
                    discount_amount = (line.price_unit * line.quantity) * (line.discount / 100.0)
                    total_discount += discount_amount

            move.total_discount = float_round(total_discount, precision_rounding=currency.rounding)