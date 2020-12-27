# -*- coding: utf-8 -*-
{
    'name': "WorkorderQueue",

    'summary': """
      Work Order Queue menu""",

    'description': """
      This menu show a list view of sale order lines.The user can able to Filter by Materials received,Group by machines 
      and sales order and Sort by the delivery date
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'machines'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
