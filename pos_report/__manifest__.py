# -*- coding: utf-8 -*-
{
    'name': "pos_report",

    'summary': """
        Excel report creation in pos module Sale detail""",

    'description': """
        Create a excel report of the sale details in the point of sale module. A button is added to print excel report 
        is added to the Sale details wizard to print the excel report.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/wizard.xml',
        'static/src/js/action_manager.xml'
    ],

}
