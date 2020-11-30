# -*- coding: utf-8 -*-
# from odoo import http


# class H(http.Controller):
#     @http.route('/h/h/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/h/h/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('h.listing', {
#             'root': '/h/h',
#             'objects': http.request.env['h.h'].search([]),
#         })

#     @http.route('/h/h/objects/<model("h.h"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('h.object', {
#             'object': obj
#         })
