# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request


class ScarpManagement(models.Model):
    _inherit = 'stock.scrap'
    _description = 'Scrap Management'

    @api.onchange('product_id')
    def value_pc(self):
        product = self.product_id
        product_int = int(product)
        loc = request.env['stock.putaway.rule'].search([('product_id', '=', product_int)])
        for rec in loc:
            self.location_id = rec.location_out_id
