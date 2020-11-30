# -*- coding: utf-8 -*-
# from odoo import http


# class ProductReservation(http.Controller):
#     @http.route('/product_reservation/product_reservation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_reservation/product_reservation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_reservation.listing', {
#             'root': '/product_reservation/product_reservation',
#             'objects': http.request.env['product_reservation.product_reservation'].search([]),
#         })

#     @http.route('/product_reservation/product_reservation/objects/<model("product_reservation.product_reservation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_reservation.object', {
#             'object': obj
#         })
