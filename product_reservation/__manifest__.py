# -*- coding: utf-8 -*-
{
    'name': "ProductReservation",

    'summary': """
        This module allows to reserve product and the needed quantity""",

    'description': """
        This module allows to reserve product and the needed quantity.Reservation is added to the sale order form,while 
        selecting reservation name from there,order lines are populated with details of reservation
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
        'data/sequence.xml',
        'data/cron_job.xml',
        'views/product_reservation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
