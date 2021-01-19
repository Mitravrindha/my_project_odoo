# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosButton(models.Model):
    _inherit = 'pos.config'

    pay = fields.Selection([
        ('disc', 'Discount Percentage'),
        ('amt', 'Amount'),
    ], string='Payment')
    en_discount = fields.Boolean(string="Enable Discount")
    disc_product_id = fields.Many2one('product.product', string='Discount Product',
                                      domain="[('available_in_pos', '=', True), ('sale_ok', '=', True)]",
                                      help='The product used to model the discount.')
