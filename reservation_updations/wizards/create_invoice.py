from odoo import models, fields, api


class CreateInvoices(models.TransientModel):
    _name = 'reservation.invoices'

    reserved_ids = fields.Many2many('product.reservation', string="Reservations")

    def reserve_invoice(self):
        list = []
        invoice_date = fields.datetime.today()
        for rec in range(len(self.reserved_ids)):
            reserve_lines = []
            for lines in self.reserved_ids[rec].reservation_lines:
                reserve_lines.append(
                    [0, 0, {'product_id': lines.product_id, 'product_uom_id': lines.product_id.uom_id,
                            'price_unit': lines.product_id.lst_price, 'quantity': lines.product_qty}])
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.reserved_ids[rec].customer_id,
                'invoice_date': invoice_date,
                'invoice_line_ids': reserve_lines,
                'reference_id': self.reserved_ids[rec]
            })
            invoiced_id = int(invoice)
            list.append(invoiced_id)

        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'res_id': list,
            'target': 'current',
            'domain': [('id', '=', list)]

        }


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    invoiced_id = fields.Integer(string="Reference")
    reference_id = fields.Many2one('product.reservation', string="Reservation Reference")

    def action_post(self):
        res = super(AccountMoveInherit, self).action_post()
        inv = self.env['product.reservation']
        self.reference_id.inv_ref = self.id
        return res
