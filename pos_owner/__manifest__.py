# -*- coding: utf-8 -*-
{
    'name': "POS Owner",

    'summary': """
        Product Owner is added to the products""",

    'description': """
         Product Owner is added to the products and displayed in pos order lines and pos receipt.
    """,

    'depends': ['base', 'sale', 'point_of_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/pos_owner.xml',

    ],
    'qweb': ['static/src/xml/pos_receipt.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
