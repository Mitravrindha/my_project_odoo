from odoo import models, fields, api


class CreateInvoices(models.TransientModel):
    _name = 'reservation.invoices'

    reserved_ids = fields.Many2many('product.reservation', string="Reservations")

    def reserve_invoice(self):
        val = []
        lis = []
        invoice_date = fields.datetime.today()
        for rec in self.reserved_ids:
            reserve_lines = []
            for lines in rec.reservation_lines:
                reserve_lines.append(
                    [0, 0, {'product_id': lines.product_id, 'product_uom_id': lines.product_id.uom_id,
                            'price_unit': lines.product_id.lst_price, 'quantity': lines.product_qty}])
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec.customer_id,
                'invoice_date': invoice_date,
                'invoice_line_ids': reserve_lines,
                'inv_id': rec
            })
            lis.append([(invoice.inv_id, '=', rec)])
            invoiced_id = int(invoice)
            val.append(invoiced_id)

        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'res_id': lis,
            'target': 'current',
            'domain': [('id', '=', val)]

        }


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    inv_id = fields.Many2one('product.reservation', string="Reservation Reference")

    def action_post(self):
        res = super(AccountMoveInherit, self).action_post()
        self.inv_id.inv_ref = self.id
        return res
