# from odoo import models, fields, api

# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'

#     fbr_sales_tax = fields.Monetary(
#         string="Sales Tax",
#         currency_field='currency_id',
#         compute='_compute_fbr_sales_tax',
#         store=True
#     )
#     fbr_extra_tax = fields.Monetary(
#         string="Extra Tax",
#         currency_field='currency_id',
#         compute='_compute_fbr_extra_tax',
#         store=True
#     )
#     fbr_further_tax = fields.Monetary(
#         string="Further Tax",
#         currency_field='currency_id',
#         compute='_compute_fbr_further_tax',
#         store=True
#     )
#     fbr_fed_payable = fields.Monetary(
#         string="FED Payable",
#         currency_field='currency_id',
#         compute='_compute_fbr_fed_payable',
#         store=True
#     )
#     fbr_withholding_tax = fields.Monetary(
#         string="Withholding Tax",
#         currency_field='currency_id',
#         compute='_compute_fbr_withholding_tax',
#         store=True
#     )

#     # === COMPUTE METHODS ===

#     @api.depends('price_subtotal', 'tax_ids')
#     def _compute_fbr_sales_tax(self):
#         for line in self:
#             tax_amount = 0.0
#             for tax in line.tax_ids:
#                 if tax.fbr_tax_type == 'sales_tax':
#                     tax_amount += (line.price_subtotal * tax.amount) / 100
#             line.fbr_sales_tax = tax_amount

#     @api.depends('price_subtotal', 'tax_ids')
#     def _compute_fbr_extra_tax(self):
#         for line in self:
#             tax_amount = 0.0
#             for tax in line.tax_ids:
#                 if tax.fbr_tax_type == 'extra_tax':
#                     tax_amount += (line.price_subtotal * tax.amount) / 100
#             line.fbr_extra_tax = tax_amount

#     @api.depends('price_subtotal', 'tax_ids')
#     def _compute_fbr_further_tax(self):
#         for line in self:
#             tax_amount = 0.0
#             for tax in line.tax_ids:
#                 if tax.fbr_tax_type == 'further_tax':
#                     tax_amount += (line.price_subtotal * tax.amount) / 100
#             line.fbr_further_tax = tax_amount

#     @api.depends('price_subtotal', 'tax_ids')
#     def _compute_fbr_fed_payable(self):
#         for line in self:
#             tax_amount = 0.0
#             for tax in line.tax_ids:
#                 if tax.fbr_tax_type == 'fed_payable':
#                     # FED might be fixed or percentage-based
#                     if tax.amount_type == 'percent':
#                         tax_amount += (line.price_subtotal * tax.amount) / 100
#                     else:
#                         tax_amount += tax.amount
#             line.fbr_fed_payable = tax_amount

#     @api.depends('price_subtotal', 'tax_ids')
#     def _compute_fbr_withholding_tax(self):
#         for line in self:
#             tax_amount = 0.0
#             for tax in line.tax_ids:
#                 if tax.fbr_tax_type == 'withholding_tax':
#                     tax_amount += (line.price_subtotal * tax.amount) / 100
#             line.fbr_withholding_tax = tax_amount


from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    fbr_sales_tax = fields.Monetary(string="Sales Tax", compute="_compute_fbr_sales_tax")
    fbr_extra_tax = fields.Monetary(string="Extra Tax", compute="_compute_fbr_extra_tax")
    fbr_further_tax = fields.Monetary(string="Further Tax", compute="_compute_fbr_further_tax")
    fbr_fed_payable = fields.Monetary(string="FED Payable", compute="_compute_fbr_fed_payable")
    fbr_withholding_tax = fields.Monetary(string="Withholding Tax", compute="_compute_fbr_withholding_tax")

    # === SALES TAX ===
    @api.depends('price_unit', 'quantity', 'tax_ids', 'currency_id', 'product_id', 'partner_id')
    def _compute_fbr_sales_tax(self):
        for line in self:
            tax_amount = 0.0
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    line.price_unit,
                    currency=line.currency_id,
                    quantity=line.quantity,
                    product=line.product_id,
                    partner=line.partner_id
                )
                for tax_val in taxes_res['taxes']:
                    tax = line.tax_ids.filtered(lambda t: t.id == tax_val['id'])
                    if tax and tax.fbr_tax_type_id.name == 'salesTaxApplicable':
                        tax_amount += tax_val['amount']
            line.fbr_sales_tax = tax_amount

    # === EXTRA TAX ===
    @api.depends('price_unit', 'quantity', 'tax_ids', 'currency_id', 'product_id', 'partner_id')
    def _compute_fbr_extra_tax(self):
        for line in self:
            tax_amount = 0.0
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    line.price_unit,
                    currency=line.currency_id,
                    quantity=line.quantity,
                    product=line.product_id,
                    partner=line.partner_id
                )
                for tax_val in taxes_res['taxes']:
                    tax = line.tax_ids.filtered(lambda t: t.id == tax_val['id'])
                    if tax and tax.fbr_tax_type_id.name == 'extraTax':
                        tax_amount += tax_val['amount']
            line.fbr_extra_tax = tax_amount

    # === FURTHER TAX ===
    @api.depends('price_unit', 'quantity', 'tax_ids', 'currency_id', 'product_id', 'partner_id')
    def _compute_fbr_further_tax(self):
        for line in self:
            tax_amount = 0.0
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    line.price_unit,
                    currency=line.currency_id,
                    quantity=line.quantity,
                    product=line.product_id,
                    partner=line.partner_id
                )
                for tax_val in taxes_res['taxes']:
                    tax = line.tax_ids.filtered(lambda t: t.id == tax_val['id'])
                    if tax and tax.fbr_tax_type_id.name == 'furtherTax':
                        tax_amount += tax_val['amount']
            line.fbr_further_tax = tax_amount

    # === FED PAYABLE ===
    @api.depends('price_unit', 'quantity', 'tax_ids', 'currency_id', 'product_id', 'partner_id')
    def _compute_fbr_fed_payable(self):
        for line in self:
            tax_amount = 0.0
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    line.price_unit,
                    currency=line.currency_id,
                    quantity=line.quantity,
                    product=line.product_id,
                    partner=line.partner_id
                )
                for tax_val in taxes_res['taxes']:
                    tax = line.tax_ids.filtered(lambda t: t.id == tax_val['id'])
                    if tax and tax.fbr_tax_type_id.name == 'fed_payable':
                        tax_amount += tax_val['amount']
            line.fbr_fed_payable = tax_amount

    # === WITHHOLDING TAX ===
    @api.depends('price_unit', 'quantity', 'tax_ids', 'currency_id', 'product_id', 'partner_id')
    def _compute_fbr_withholding_tax(self):
        for line in self:
            tax_amount = 0.0
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    line.price_unit,
                    currency=line.currency_id,
                    quantity=line.quantity,
                    product=line.product_id,
                    partner=line.partner_id
                )
                for tax_val in taxes_res['taxes']:
                    tax = line.tax_ids.filtered(lambda t: t.id == tax_val['id'])
                    if tax and tax.fbr_tax_type_id.name == 'salesTaxWithheldAtSource':
                        tax_amount += tax_val['amount']
            line.fbr_withholding_tax = tax_amount