# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
"""Realign stale ``discount_fixed`` values on existing draft invoice lines.

Before this version the total-based fixed discount was only recomputed when the
percentage or the unit price changed, never when the quantity changed.  Lines
whose quantity was edited after the discount was entered therefore kept a
``discount_fixed`` (and resulting subtotal) computed from the old quantity.

Only *draft* moves are touched here; posted entries are left untouched and must
be corrected through the normal accounting flow (reset to draft or credit note).
"""

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    lines = env["account.move.line"].search(
        [
            ("display_type", "=", "product"),
            ("parent_state", "=", "draft"),
            ("discount", "!=", 0.0),
            ("discount_fixed", "!=", 0.0),
        ]
    )
    to_fix = env["account.move.line"]
    for line in lines:
        currency = line.currency_id or line.company_id.currency_id
        if not currency:
            continue
        expected = (line.discount / 100.0) * line.price_unit * line.quantity
        if currency.compare_amounts(expected, line.discount_fixed) != 0:
            to_fix |= line

    if to_fix:
        _logger.info(
            "account_invoice_fixed_discount_subtotal: realigning discount_fixed "
            "on %s draft invoice line(s)",
            len(to_fix),
        )
        to_fix._sync_fixed_discount_from_percentage()
