# -*- coding: utf-8 -*-
{
    'name': "Machines",

    'summary': """
       Machines List""",

    'description': """Tree view and list view of machines
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
