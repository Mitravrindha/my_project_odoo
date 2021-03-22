# -*- coding: utf-8 -*-

# from odoo import models, fields, api
#
#
# class LoanManagement(models.Model):
#     _name = 'loan.management'
#     _description = 'Loan Management'
#
#     customer_id = fields.Many2one('res.partner',string="Customer Name")
#     age = fields.Integer()
#     address = fields.Text(string="Address")
#     scheme = fields.Many2one('loan.scheme',string="Loan Type")
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
