# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReservationUpdate(models.Model):
    _name = 'reservation.update'
    _description = 'Reservation Updates'

    reserve_ids = fields.Many2many('product.reservation', 'reserved_rel', string="Reservations")


