# -*- coding: utf-8 -*-
{
    'name': "Work Order Queue",

    'summary': """
      Work Order Queue menu""",

    'description': """
      This menu show a list view of sale order lines.The user can able to Filter by Materials received,Group by machines 
      and sales order and Sort by the delivery date
    """,

    'depends': ['sale', 'machines'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
    ],

}
