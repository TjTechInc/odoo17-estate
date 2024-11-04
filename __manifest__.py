# -*- coding: utf-8 -*-
{
    'name': "estate",

    'summary': "Estate Property",

    'description': """
Estate property technical Course Odoo17
    """,

    'author': "Tinotenda Daki",
    'website': "https://www.zimhotels.com.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/estate_property_type.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_tags.xml',
        'views/estate_property.xml',

        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

