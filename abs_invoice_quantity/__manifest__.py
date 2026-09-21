# -*- coding: utf-8 -*-


{
    'name'           : "Total number of Products and Quantity on Invoices",
    'author'         : 'Ascetic Business Solution',
    'category'       : 'Account',
    'summary'        : """Display total number of Products and Quantity on Invoices""",
    'website'        : 'http://www.asceticbs.com',
    'description'    : """""",
    'version'        : '18.0.1.1.0',
    'depends'        : ['base','account', 'account_invoice_fixed_discount'],
    'data'           : [
                         'security/account_invoice_security.xml',
                         'views/account_invoice_view.xml',]
                        #  'report/account_invoice_report_templates.xml',
                        #  'views/account_report_view.xml']
                         ,
    'images'         : ['static/description/banner.png'],
    'license'        : 'AGPL-3',
    'installable'    : True,
    'application'    : True,
    'auto_install'   : False,
}
