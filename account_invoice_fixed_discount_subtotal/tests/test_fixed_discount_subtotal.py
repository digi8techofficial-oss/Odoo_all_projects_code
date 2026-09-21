# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.tests import Form, tagged
from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestFixedDiscountSubtotal(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.groups_id |= cls.env.ref("account.group_account_invoice")
        cls.env.user.groups_id |= cls.env.ref(
            "account_invoice_fixed_discount.group_fixed_discount"
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test"})
        cls.product = cls.env.ref("product.product_product_3")
        cls.account = cls.env["account.account"].search(
            [("account_type", "=", "income")], limit=1
        )
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )

    def _new_invoice(self):
        invoice_form = Form(
            self.env["account.move"].with_context(
                default_move_type="out_invoice",
                default_journal_id=self.journal.id,
            )
        )
        invoice_form.partner_id = self.partner
        with invoice_form.invoice_line_ids.new() as line:
            line.product_id = self.product
            line.account_id = self.account
            line.name = "Line 1"
            line.tax_ids.clear()
            line.price_unit = 105000.0
            line.quantity = 4.0
            line.discount = 4.0
        return invoice_form.save()

    def test_fixed_discount_follows_percentage_on_quantity(self):
        """The total-based fixed discount is recalculated when quantity changes."""
        invoice = self._new_invoice()
        line = invoice.invoice_line_ids

        # 4% of 105000 * 4
        self.assertAlmostEqual(line.discount_fixed, 16800.0, places=2)
        self.assertAlmostEqual(line.price_subtotal, 403200.0, places=2)

        with Form(invoice) as invoice_form:
            with invoice_form.invoice_line_ids.edit(0) as line_form:
                line_form.quantity = 3.0

        # 4% of 105000 * 3 -> discount amount must shrink with the quantity
        self.assertAlmostEqual(line.discount, 4.0, places=2)
        self.assertAlmostEqual(line.discount_fixed, 12600.0, places=2)
        self.assertAlmostEqual(line.price_subtotal, 302400.0, places=2)

    def test_quantity_write_resyncs_fixed_discount(self):
        """A plain write() on quantity also realigns the fixed discount."""
        invoice = self._new_invoice()
        line = invoice.invoice_line_ids
        self.assertAlmostEqual(line.discount_fixed, 16800.0, places=2)

        line.write({"quantity": 3.0})

        self.assertAlmostEqual(line.discount_fixed, 12600.0, places=2)
        self.assertAlmostEqual(line.price_subtotal, 302400.0, places=2)
