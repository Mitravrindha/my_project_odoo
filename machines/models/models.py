# -*- coding: utf-8 -*-

from odoo import models, fields, api
class machines(models.Model):

    _name = 'machines.list'
    _description = 'machines.machines'
    _rec_name = 'machine_name'

    machine_name = fields.Char(string="Machine name")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
