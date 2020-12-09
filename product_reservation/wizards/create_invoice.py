from odoo import models, fields, api


class CreateInvoices(models.TransientModel):
    _name = 'create.invoices'

    reserved_ids = fields.Many2many('product.reservation', string="Reservations")

    def create_invoices(self):
        print("hello button")
        product_env = self.env['product.reservation']
        reserve_lines = []
        seq = []
        invoice_date = fields.datetime.today()

        for rec in self:
            for i in self.reserved_ids:
                print(self.reserved_ids)
                for r in i.reservation_lines:
                    reserve_lines.append(
                        [0, 0, {'product_id': r.product_id, 'product_uom_id': r.product_id.uom_id,
                                'price_unit': r.product_id.lst_price, 'quantity': r.product_qty}])
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.reserved_ids.customer_id,
            'invoice_date': invoice_date,
            'invoice_line_ids': reserve_lines,
            'invoiced_id': self.reserved_ids,

        })
        print(invoice)

        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': int(invoice),
            'target': 'current',
            'domain': []

        }


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    invoiced_id = fields.Many2many('product.reservation', string="Invoice Reference")

    def action_post(self):
        res = super(AccountMoveInherit, self).action_post()
        inv = self.env['product.reservation']
        self.invoiced_id.inv_ref = self.id
        return res


class SalesPersonReport(models.TransientModel):
    _name = 'person.report'

    person_id = fields.Many2one('res.users', string="Sales Person")
    person_date = fields.Date(string="Date")
