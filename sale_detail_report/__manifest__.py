# -*- coding: utf-8 -*-
{
    'name': "Sale Report",

    'summary': """
       A menu Create Reports is added to produce the sale detail report,there is a provision to filter it using the 
       salesperson and order date""",

    'description': """
        Long description of module's purpose
    """,

    'depends': ['contacts', 'sale', 'base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'reports/report.xml',
        'reports/templates.xml',
        'views/views.xml',
        'wizards/wizard.xml'
    ],
}
