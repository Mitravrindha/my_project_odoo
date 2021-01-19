# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OwnerName(models.Model):
    _name = 'owner.name'
    _description = 'Owner Names'

    _rec_name = 'name'

    name = fields.Char(string="Owner Name")


class PosOwner(models.Model):
    _inherit = 'product.product'
    _rec_name = 'owner_name'

    owner_name = fields.Many2one('owner.name', string="Product Owner")

