# -*- coding: utf-8 -*-
{
    'name': "Sale Report",

    'summary': """
       A menu Create Reports is added to produce the sale detail report,there is a provision to filter it using the 
       salesperson and order date""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts', 'sale', 'base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/report.xml',
        'reports/templates.xml',
        'views/views.xml',
        'wizards/wizard.xml'
    ],
}
