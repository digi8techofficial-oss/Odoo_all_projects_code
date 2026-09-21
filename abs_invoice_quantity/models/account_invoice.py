# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2024-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"

    total_product = fields.Integer(string='Total Product:',compute='_total_product',help="total Products")
    total_quantity = fields.Integer(string='Total Quantity:',compute='_total_quantity',help="total Quantity")
    total_discount_fixed = fields.Monetary(string='Total Fixed Discount:', compute='_compute_total_discount_fixed', currency_field='currency_id')
    total_amount_before_discount = fields.Monetary(string='Total Amount Before Discount:', compute='_compute_total_amount_before_discount', currency_field='currency_id', help="Untaxed amount of the product lines before any discount")

    @api.depends('invoice_line_ids.quantity', 'invoice_line_ids.price_unit')
    def _compute_total_amount_before_discount(self):
        for record in self:
            record.total_amount_before_discount = sum(
                line.quantity * line.price_unit
                for line in record.invoice_line_ids
                if line.display_type == 'product'
            )

    @api.depends('invoice_line_ids.discount_fixed')
    def _compute_total_discount_fixed(self):
        for record in self:
            total = sum(line.discount_fixed for line in record.invoice_line_ids)
            record.total_discount_fixed = total

    @api.depends('invoice_line_ids')
    def _total_product(self):
        for record in self:
            product_list=[]
            for line in record.invoice_line_ids:
                product_list.append(line.product_id)
            record.total_product = len(set(product_list))

    @api.depends('invoice_line_ids.quantity')
    def _total_quantity(self):
        for record in self:
            total_qty = 0
            for line in record.invoice_line_ids:
                total_qty = total_qty + line.quantity
            record.total_quantity = total_qty
