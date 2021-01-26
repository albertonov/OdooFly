# -*- coding: utf-8 -*-
from openerp import http

# class Odoofly(http.Controller):
#     @http.route('/odoofly/odoofly/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoofly/odoofly/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoofly.listing', {
#             'root': '/odoofly/odoofly',
#             'objects': http.request.env['odoofly.odoofly'].search([]),
#         })

#     @http.route('/odoofly/odoofly/objects/<model("odoofly.odoofly"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoofly.object', {
#             'object': obj
#         })