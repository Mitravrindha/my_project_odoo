# -*- coding: utf-8 -*-
# from odoo import http


# class Machines(http.Controller):
#     @http.route('/machines/machines/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/machines/machines/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('machines.listing', {
#             'root': '/machines/machines',
#             'objects': http.request.env['machines.machines'].search([]),
#         })

#     @http.route('/machines/machines/objects/<model("machines.machines"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('machines.object', {
#             'object': obj
#         })
