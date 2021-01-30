from odoo import http
from odoo.http import request


class RepairForm(http.Controller):

    @http.route('/repair_order', type="http", auth='public', website=True)
    def repair_order(self, **kw):
        product_rec = request.env['product.product'].sudo().search([])
        partner_rec = request.env.user.partner_id
        users_rec = request.env['res.users'].sudo().search([])
        location_rec = request.env['stock.location'].sudo().search([])
        uo_rec = request.env['repair.order'].sudo().search([])
        uom_rec = uo_rec.mapped('product_uom')
        print(partner_rec)
        print(users_rec.mapped('partner_id'))
        if partner_rec in users_rec.mapped('partner_id'):
            print("hello")

        return http.request.render('repair_form.repair_form',
                                   {'products': product_rec, 'partners': partner_rec, 'users': users_rec,
                                    'locations': location_rec, 'measures': uom_rec})

    @http.route('/create/repair_form', type="http", auth='public', website=True)
    def create_order(self, **kw):
        print(kw)
        request.env['repair.order'].sudo().create(kw)
        return request.render("repair_form.repair_thanks", {})
