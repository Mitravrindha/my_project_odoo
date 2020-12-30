# -*- coding: utf-8 -*-
{
    'name': "Reservation Updations",

    'summary': """
       Invoices are created for selected reservations""",

    'description': """
        A menu item create invoices is added to the sales module.By selecting the multiple reservations we can create 
        invoices for those reservations.While confirming the invoice the invoice reference is added to the reservation form.
    """,

    'depends': ['base', 'product_reservation'],

    'data': [
        'security/ir.model.access.csv',
        'wizards/create_invoice.xml',
    ],
}
