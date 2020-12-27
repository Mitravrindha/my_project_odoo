# -*- coding: utf-8 -*-
{
    'name': "Reservation Updations",

    'summary': """
       Invoices are created for selected reservations""",

    'description': """
        A menu item create invoices is added to the sales module.By selecting the multiple reservations we can create 
        invoices for those reservations.While confirming the invoice the invoice reference is added to the reservation form.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product_reservation'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/create_invoice.xml',
    ],
}
