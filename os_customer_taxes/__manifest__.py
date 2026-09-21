{
    'name': 'Customer Taxes',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Add extra taxes to contacts and apply them on invoice lines',
    'description': """
        This module adds an "Extra Taxes" field to the functionality of the Contact form.
        When creating an invoice line, taxes from the product are fetched as usual,
        but additionally, any taxes specified on the customer (Contact) are also added.
        Duplicate taxes are avoided.
    """,
    'author': 'Usman F.',
    'depends': ['account', 'sale'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
