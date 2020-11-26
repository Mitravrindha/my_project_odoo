# -*- coding: utf-8 -*-
from odoo import models, fields, api


class WorkorderQueue(models.Model):
    _name = 'workorder.queue'
    _description = 'work_order.queue'
    machine_name = fields.Many2one("machines.list", string="Machine Name")
    delivery_date = fields.Date(string="Delivery_date")
    materials_recieved = fields.Boolean(string="Materials_Recieved")


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order.line'
    _order = 'delivery_date desc'
    machine_name = fields.Many2one("machines.list", string="Machine Name")
    delivery_date = fields.Date(string="Delivery Date")
    materials_recieved = fields.Boolean(string="Materials Recieved")



class SaleOrderViewInherit(models.Model):
     _inherit = 'sale.order'
     machine_name = fields.Many2one("machines.list", string="Machine Name")
     delivery_date = fields.Date(string="Delivery Date")
     materials_recieved = fields.Boolean(string="Materials Recieved")

#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
