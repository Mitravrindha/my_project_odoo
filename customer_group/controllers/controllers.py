# # -*- coding: utf-8 -*-
# from odoo import http
# from odoo.http import request
# from odoo.addons.website.controllers.main import QueryURL
# from odoo.addons.website_sale.controllers.main import WebsiteSale
#
#
# def sitemap_shop(env, rule, qs):
#     if not qs or qs.lower() in '/shop':
#         yield {'loc': '/shop'}
#     category = env['product.public.category']
#     dom = sitemap_qs2dom(qs, '/shop/category', category._rec_name)
#     dom += env['website'].get_current_website().website_domain()
#     for cat in category.search(dom):
#         loc = '/shop/category/%s' % slug(cat)
#         if not qs or qs.lower() in loc:
#             yield {'loc': loc}
#
#
# def reset_domain(self, search, categories, available_products, attrib_values, search_in_description=True):
#     '''
#     Function returns a domain consist of filter conditions
#     :param search: search variable
#     :param categories: list of category available
#     :param available_products: list of available product ids from product.template
#     :param attrib_values:product attiribute values
#     :param search_in_description: boolean filed showing there is search variable exist or not'''
#
#     domains = [request.website.sale_product_domain()]
#     if search:
#         for srch in search.split(" "):
#             subdomains = [
#                 [('name', 'ilike', srch)],
#                 [('product_variant_ids.default_code', 'ilike', srch)]
#             ]
#             if search_in_description:
#                 subdomains.append([('description', 'ilike', srch)])
#                 subdomains.append([('description_sale', 'ilike', srch)])
#             domains.append(expression.OR(subdomains))
#     if available_products:
#         domains.append([('id', 'in', available_products.ids)])
#     if categories:
#         domains.append([('public_categ_ids', 'child_of', categories.ids)])
#     if attrib_values:
#         attrib = None
#         ids = []
#         for value in attrib_values:
#             if not attrib:
#                 attrib = value[0]
#                 ids.append(value[1])
#             elif value[0] == attrib:
#                 ids.append(value[1])
#             else:
#                 domains.append([('attribute_line_ids.value_ids', 'in', ids)])
#                 attrib = value[0]
#                 ids = [value[1]]
#         if attrib:
#             domains.append([('attribute_line_ids.value_ids', 'in', ids)])
#
#     return expression.AND(domains)
#
#
# class WebsiteSaleInherit(WebsiteSale):
#     @http.route([
#         '''/shop''',
#         '''/shop/page/<int:page>''',
#         '''/shop/category/<model("product.public.category"):category>''',
#         '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
#     ], type='http', auth="public", website=True)
#     def shop(self, page=0, category=None, search='', ppg=False, **post):
#         res = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', ppg=False, **post)
#         available_categ = available_products = ''
#         user = request.env['res.users'].sudo().search([('id', '=', request.env.user.id)])
#         mode = user.customer_group_id.category_name_ids
#         if mode:
#             available_categ = mode
#             print(available_categ)
#
#         Category_avail = []
#         Category = request.env['product.public.category']
#         for ids in available_categ:
#             if not ids.parent_id.id in available_categ.ids:
#                 Category_avail.append(ids.id)
#         categ = request.env['product.public.category'].search([('id', 'in', Category_avail)])
#         print(categ)
#
#         if not available_categ and not available_products:
#             return super(ProductVisibilityCon, self).shop(page, category, search, ppg, **post)
#         add_qty = int(post.get('add_qty', 1))
#
#         if category:
#             category = Category.search([('id', '=', int(category))], limit=1)
#             if not category or not category.can_access_from_current_website():
#                 raise NotFound()
#         else:
#             category = Category
#
#             if ppg:
#                 try:
#                     ppg = int(ppg)
#                     post['ppg'] = ppg
#                 except ValueError:
#                     ppg = False
#             if not ppg:
#                 ppg = request.env['website'].get_current_website().shop_ppg or 20
#             ppr = request.env['website'].get_current_website().shop_ppr or 4
#             attrib_list = request.httprequest.args.getlist('attrib')
#             attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
#             attributes_ids = {v[0] for v in attrib_values}
#             attrib_set = {v[1] for v in attrib_values}
#             domain = self._get_search_domain(search, category, attrib_values)
#             Product = request.env['product.template'].with_context(bin_size=True)
#             if available_products:
#                 domain_pro = self.reset_domain(search, category, available_products, attrib_values)
#                 Product = Product.search(domain_pro)
#             keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
#                             order=post.get('order'))
#             pricelist_context, pricelist = self._get_pricelist_context()
#             request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
#             url = "/shop"
#             if search:
#                 post["search"] = search
#             if attrib_list:
#                 post['attrib'] = attrib_list
#             if not category:
#                 domain = self.reset_domain(search, available_categ, available_products, attrib_values)
#             search_product = Product.search(domain)
#             website_domain = request.website.website_domain()
#             categs_domain = [('parent_id', '=', False), ('product_tmpl_ids', 'in', search_product.ids)] + website_domain
#             if search:
#                 search_categories = Category.search(
#                     [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
#                 categs_domain.append(('id', 'in', search_categories.ids))
#             else:
#                 search_categories = available_categ
#             if category:
#                 url = "/shop/category/%s" % slug(category)
#             product_count = len(search_product)
#             pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
#             products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))
#             if not category:
#                 if available_products:
#                     products = Product.search(domain_pro, limit=ppg, offset=pager['offset'],
#                                               order=self._get_search_order(post))
#                 else:
#                     products = Product.search(domain, limit=ppg, offset=pager['offset'],
#                                               order=self._get_search_order(post))
#             else:
#                 if available_products:
#                     products = Product.search(domain_pro, limit=ppg, offset=pager['offset'],
#                                               order=self._get_search_order(post))
#                 else:
#                     products = Product.search(domain, limit=ppg, offset=pager['offset'],
#                                               order=self._get_search_order(post))
#             ProductAttribute = request.env['product.attribute']
#             if products:
#                 # get all products without limit
#                 attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
#             else:
#                 attributes = ProductAttribute.browse(attributes_ids)
#
#             layout_mode = request.session.get('website_sale_shop_layout_mode')
#             if not layout_mode:
#                 if request.website.viewref('website_sale.products_list_view').active:
#                     layout_mode = 'list'
#                 else:
#                     layout_mode = 'grid'
#             values = {
#                 'search': search,
#                 'category': category,
#                 'attrib_values': attrib_values,
#                 'attrib_set': attrib_set,
#                 'pager': pager,
#                 'pricelist': pricelist,
#                 'add_qty': add_qty,
#                 'products': products,
#                 'search_count': product_count,  # common for all searchbox
#                 'bins': TableCompute().process(products, ppg, ppr),
#                 'ppg': ppg,
#                 'ppr': ppr,
#                 'categories': categ,
#                 'attributes': attributes,
#                 'keep': keep,
#                 'search_categories_ids': categ.ids,
#                 'layout_mode': layout_mode,
#             }
#
#             if category:
#                 values['main_object'] = category
#             return request.render("website_sale.products", values)
#
#         def availavle_products(self):
#             ''''Returns the available product (product.template) ids'''
#             user = request.env['res.users'].sudo().search([('id', '=', request.env.user.id)])
#             return user.customer_group_id.category_name_ids
#
#         return res
#
# # class CustomerGroup(http.Controller):
# #     @http.route('/customer_group/customer_group/', auth='public')
# #     def index(self, **kw):
# #         return "Hello, world"
#
# #     @http.route('/customer_group/customer_group/objects/', auth='public')
# #     def list(self, **kw):
# #         return http.request.render('customer_group.listing', {
# #             'root': '/customer_group/customer_group',
# #             'objects': http.request.env['customer_group.customer_group'].search([]),
# #         })
#
# #     @http.route('/customer_group/customer_group/objects/<model("customer_group.customer_group"):obj>/', auth='public')
# #     def object(self, obj, **kw):
# #         return http.request.render('customer_group.object', {
# #             'object': obj
# #         })
