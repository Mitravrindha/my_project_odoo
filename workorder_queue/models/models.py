# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order.line'
    _order = 'delivery_date desc'
    machine_name = fields.Many2one("machines.list", string="Machine Name")
    delivery_date = fields.Date(string="Delivery Date")
    materials_recieved = fields.Boolean(string="Materials Recieved")
