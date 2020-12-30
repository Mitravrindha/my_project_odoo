# -*- coding: utf-8 -*-
{
    'name': "POS Excel Report",

    'summary': """
        Excel report creation in pos module Sale detail""",

    'description': """
        Create a excel report of the sale details in the point of sale module. A button is added to print excel report 
        is added to the Sale details wizard to print the excel report.
    """,

    'depends': ['base', 'point_of_sale'],

    'data': [
        'security/ir.model.access.csv',
        'wizards/wizard.xml',
        'views/action_manager.xml'
    ],

}
