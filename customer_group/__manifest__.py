# -*- coding: utf-8 -*-
{
    'name': "Customer Group",

    'summary': """
    Create Customer Groups""",

    'description': """
        Create Customer Groups and a  Option to add Product Categories for Customer groups. When a customer login only show
        the products related to his  group. If a customer has no group, no products will show    """,

    'depends': ['base', 'sale', 'website', 'website_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

}
