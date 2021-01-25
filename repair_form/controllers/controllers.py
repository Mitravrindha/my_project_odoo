from odoo import http
from odoo.http import request


class RepairForm(http.Controller):

    @http.route('/repair_order', type="http", auth='public', website=True)
    def repair_order(self, **kw):
        product_rec = request.env['product.template'].search([])
        partner_rec = request.env['res.partner'].search([])
        users_rec = request.env['res.users'].search([])
        location_rec = request.env['stock.location'].search([])
        # uom_rec = request.env['uom.uom'].search([])
        uo_rec = request.env['repair.order'].search([])
        uom_rec = uo_rec.mapped('product_uom')

        print(uo_rec.mapped('product_uom'))
        return http.request.render('repair_form.repair_form',
                                   {'products': product_rec, 'partners': partner_rec, 'users': users_rec,
                                    'locations': location_rec, 'measures': uom_rec})

    @http.route('/create/repair_form', type="http", auth='public', website=True)
    def create_order(self, **kw):
        print(kw)
        # print(kw.get('product_id.product_uom'))
        # repair_val = {
        #     'product_uom': kw.get('product.uom_po_id.id'),
        #     # 'product_qty': kw.get('product_qty'),
        #     # 'partner_id': kw.get('partner_id'),
        #     # 'user_id': kw.get('user_id')
        #
        # }
        request.env['repair.order'].create(kw)
        return request.render("repair_form.repair_thanks", {})
