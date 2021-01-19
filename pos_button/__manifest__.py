# -*- coding: utf-8 -*-
{
    'name': "POS Button",

    'summary': """
        Payment Option button  is added to the pos""",

    'description': """
         Product Owner is added to the products and displayed in pos order lines and pos receipt.
    """,

    'depends': ['base', 'sale', 'point_of_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/pos_button.xml',

    ],
    'qweb': ['static/src/xml/pos_button.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
