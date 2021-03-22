# -*- coding: utf-8 -*-
{
    'name': "Paytrail Gateway Ecommerce",

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_sale', 'website', 'account', 'payment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/paytrail_acquirer.xml',
    ],

}
