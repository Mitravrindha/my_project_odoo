# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import _


class ProductReservation(models.Model):
    _name = 'product.reservation'
    _rec_name = 'reservation_seq'

    reservation_name = fields.Char(string="Name of Reservation")
    customer_id = fields.Many2one('res.partner', string="Customer Name")
    expiry_date = fields.Date(string="Expiry Date")
    reservation_lines = fields.One2many('product.reservation.lines', 'reservation_id', string="Reservation Lines")
    note = fields.Text('Internal Note')
    reservation_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                                  default=lambda self: _('New'))

    # so_id = fields.Many2one('sale.order')

    @api.model
    def create(self, vals):
        if vals.get('reservation_seq', _('New')) == _('New'):
            vals['reservation_seq'] = self.env['ir.sequence'].next_by_code('product.reservation.sequence') or _('New')
        result = super(ProductReservation, self).create(vals)
        return result


class ProductReservationLines(models.Model):
    _name = 'product.reservation.lines'
    product_id = fields.Many2one('product.product', string="Product")
    product_qty = fields.Integer(string="Quantity")
    product_price = fields.Integer(string="Price")
    reservation_id = fields.Many2one('product.reservation', string="Reservation Id")


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    def open_reservation(self):
        print("hello button")

        return {
            'name': _('Reservations'),
            'domain': [('customer_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'product.reservation',
            'view_id': False,
            'view_type': 'form',
        }


class SaleReservationInherit(models.Model):
    _inherit = 'sale.order'

    reservation_name = fields.Many2one('product.reservation', string="Name of Reservation")
    # reserve_id = fields.One2many('product.reservation.lines', 'reservation_id', string="Reservation Lines")

    # @api.onchange('reservation_name')
        # line_env = self.env['sale.order.line']
        # for wizard in self:
        #     new_line = line_env.create({
        #             'product_id': product_id.id,
        #             'name': what.product_id.name,
        #             'order_id': what.sale_order_id.id,
        #             'product_uom': what.product_id.uom_id.id})


                # for rec in self:
        #     lines =[]
        #     print("self.reservation_name",self.reservation_name)


# reserve_id = fields.One2many('product.reservation', 'so_id')

# @api.depends('reservation_name')
# def onchange_reservation_name(self):
#     for rec in self:
#         rec.pack_id = [(6, 0, rec.reservation_name)]

#
#
# class SaleOrderFormInherit(models.Model):
#     _inherit = 'sale.order'
#     package_ids = fields.Many2many('sales.package', string="Packages",
#                                    required=True)
#     pack_id = fields.One2many('sales.package', 'so_id')
#
#     @api.onchange('package_ids')
#     def _onchange_package_ids(self):
#
#         for rec in self:
#         print("pack_id", rec.package_ids.ids)
#     rec.pack_id = [(6, 0, rec.package_ids.ids)]
