# -*- coding: utf-8 -*-
# from odoo import http


# class WorkorderQueue(http.Controller):
#     @http.route('/workorder_queue/workorder_queue/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/workorder_queue/workorder_queue/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('workorder_queue.listing', {
#             'root': '/workorder_queue/workorder_queue',
#             'objects': http.request.env['workorder_queue.workorder_queue'].search([]),
#         })

#     @http.route('/workorder_queue/workorder_queue/objects/<model("workorder_queue.workorder_queue"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('workorder_queue.object', {
#             'object': obj
#         })
