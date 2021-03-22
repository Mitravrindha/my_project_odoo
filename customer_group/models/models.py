# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomerGroup(models.Model):
    _name = 'customer.group'
    _description = 'Customer Group'
    _rec_name = 'group_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    group_name = fields.Char(string="Group Name")
    category_name_ids = fields.Many2many('product.public.category', string="Category")


class CustomerGroupInherit(models.Model):
    _inherit = 'res.partner'

    customer_group_id = fields.Many2one('customer.group', string="Customer Group")
    product_visible = fields.Boolean(string="All Product Visibility")
