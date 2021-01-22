# -*- coding: utf-8 -*-
# from odoo import http


# class RepairForm(http.Controller):
#     @http.route('/repair_form/repair_form/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/repair_form/repair_form/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('repair_form.listing', {
#             'root': '/repair_form/repair_form',
#             'objects': http.request.env['repair_form.repair_form'].search([]),
#         })

#     @http.route('/repair_form/repair_form/objects/<model("repair_form.repair_form"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('repair_form.object', {
#             'object': obj
#         })
