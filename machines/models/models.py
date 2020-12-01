# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MachinesList(models.Model):
    _name = 'machines.list'
    _description = 'Machines List'
    _rec_name = 'machine_name'

    machine_name = fields.Char(string="Machine name")
