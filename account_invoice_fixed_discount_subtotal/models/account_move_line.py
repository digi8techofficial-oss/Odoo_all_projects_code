
from odoo import models, api
from odoo.tools.float_utils import float_is_zero


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange("discount", "quantity")
    def _onchange_discount(self):
        """Keep the fixed discount amount in sync with the discount percentage.

        In this module ``discount_fixed`` represents the *total* discount of the
        line (``discount % * price_unit * quantity``).  It therefore has to be
        recomputed not only when the percentage changes but also when the
        quantity changes.

        The base module only recomputes ``discount_fixed`` on ``discount`` /
        ``price_unit`` changes, so editing the quantity used to leave a stale
        ``discount_fixed`` behind: the line totals (which are derived from
        ``discount_fixed`` in ``_compute_totals``) were then computed from the
        old amount while the displayed ``Disc.%`` still showed the original
        percentage.
        """
        if self.env.context.get("ignore_discount_onchange"):
            return
        self.env.context = self.with_context(ignore_discount_onchange=True).env.context

        # Calculate Fixed Amount = (Percentage / 100) * Line Total
        total_price = self.price_unit * self.quantity
        self.discount_fixed = (self.discount / 100.0) * total_price

    def _get_discount_from_fixed_discount(self):
        """Calculate the discount percentage from the fixed discount amount.

        Overridden to calculate based on TOTAL price (price_unit * quantity)
        instead of just price_unit.
        """
        self.ensure_one()
        currency = self.currency_id or self.company_id.currency_id
        if float_is_zero(
            self.discount_fixed, precision_rounding=currency.rounding
        ):
            return 0.0

        # Calculate total price (unit price * quantity)
        total_price = self.price_unit * self.quantity

        if float_is_zero(total_price, precision_rounding=currency.rounding):
            return 0.0

        # Percentage = (Fixed / Total) * 100
        return (self.discount_fixed / total_price) * 100

    def _sync_fixed_discount_from_percentage(self):
        """Realign ``discount_fixed`` with the percentage discount.

        Safety net for write paths that do not trigger form onchanges
        (imports, ``env['account.move.line'].write(...)``, server actions...).
        Only runs when a percentage discount is set and ``discount_fixed`` was
        not explicitly provided in the same operation.
        """
        for line in self:
            currency = line.currency_id or line.company_id.currency_id
            if not currency:
                continue
            if float_is_zero(line.discount, precision_rounding=0.01):
                continue
            expected = (line.discount / 100.0) * line.price_unit * line.quantity
            if currency.compare_amounts(expected, line.discount_fixed) != 0:
                line.discount_fixed = expected

    def write(self, vals):
        res = super().write(vals)
        if "quantity" in vals and "discount" not in vals and "discount_fixed" not in vals:
            self.filtered(
                lambda l: l.display_type == "product"
            )._sync_fixed_discount_from_percentage()
        return res
