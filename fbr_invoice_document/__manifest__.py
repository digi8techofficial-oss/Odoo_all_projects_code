{
    'name': 'FBR Digital Invoicing Connector (DI) Invoice Report',
    'version': '18.0.3.0.7',
    'summary': 'Full integration with FBR Digital Invoicing API (Validate & Post).',
    'description': """
        Update on Extra Tax Value:
        - The extra tax value is now formatted based on the sale type.
        - Button only visible in customer invoice and refund.
    """,
    'author': 'Usman Farzand',
    'company': 'Odoo Specialist',
    'maintainer': 'Usman Farzand',
    'email': 'usman@odoospecialist.com',
    'website': 'https://www.odoospecialist.com',
    'category': 'Accounting/Localizations/EDI',
    'depends': [
        'account','os_fbr_connector'
    ],
    'data': [
        'views/invoice_template.xml',
        'views/res_company_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}