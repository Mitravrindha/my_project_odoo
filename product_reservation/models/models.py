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
    sale_ref = fields.Many2one('sale.order', string="Sale Order Reference")

    @api.constrains('expiry_date')
    def expiry_check(self):
        self.search([('expiry_date', '<', fields.Datetime.now())]).unlink()

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

    @api.onchange('reservation_name')
    def _onchange_reservation_name(self):
        line_env = self.env['sale.order.line']
        # print("self.reservation_name", self.reservation_name)
        sale_lines = [(5, 0, 0)]
        for rec in self.reservation_name.reservation_lines:
            sale_lines.append(
                [0, 0, {'product_id': rec.product_id.id, 'product_uom_qty': rec.product_qty,
                        'price_unit': rec.product_id.lst_price, 'product_uom': rec.product_id.uom_id,
                        'name': rec.product_id.default_code}])
            print(rec.product_id.uom_id)
        self.order_line = sale_lines

    def action_confirm(self):
        res = super(SaleReservationInherit, self).action_confirm()
        reserve = self.env['product.reservation']
        self.reservation_name.sale_ref = self.id
        print(self.reservation_name.sale_ref)
        print(self.name)
        return res

# def default_get(self, fields):
#     res = super(AccountInvoiceSend, self).default_get(fields)
#     res_ids = self._context.get('active_ids')
#
#     invoices = self.env['account.move'].browse(res_ids).filtered(
#         lambda move: move.is_invoice(include_receipts=True))
#     if not invoices:
#         raise UserError(_("You can only send invoices."))
#
#     composer = self.env['mail.compose.message'].create({
#         'composition_mode': 'comment' if len(res_ids) == 1 else 'mass_mail',
#     })
#     res.update({
#         'invoice_ids': res_ids,
#         'composer_id': composer.id,
#     })
#     return res
