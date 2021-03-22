# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesBoolean(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Boolean Field'

    sale_bool = fields.Boolean(string="Nnog niet verzenden")


class DeliveryBoolean(models.Model):
    _inherit = 'stock.picking'
    _description = 'Delivery Boolean Field'

    # sales_id = fields.Many2one()
    delivery_bool = fields.Boolean(related='sale_id.sale_bool', string="Nnog niet verzenden", default=False,readonly=True)
