# -*- coding: utf-8 -*-
# from odoo import http


# class SaleBoolean(http.Controller):
#     @http.route('/sale_boolean/sale_boolean/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_boolean/sale_boolean/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_boolean.listing', {
#             'root': '/sale_boolean/sale_boolean',
#             'objects': http.request.env['sale_boolean.sale_boolean'].search([]),
#         })

#     @http.route('/sale_boolean/sale_boolean/objects/<model("sale_boolean.sale_boolean"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_boolean.object', {
#             'object': obj
#         })
