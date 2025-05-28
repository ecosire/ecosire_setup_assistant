# -*- coding: utf-8 -*-
{
    'name': 'Odoo Setup Assistant',
    'module_name': 'odoo_setup_assistant',
    'version': '1.1', # Incremented version for new features
    'summary': 'Diagnose Odoo setup, configuration, dependencies, and manage addon Python requirements.',
    'description': 'static/description/index.html',
    'author': 'ECOSIRE (PRIVATE) LIMITED',
    'website': 'https://www.ecosire.com/',
    'category': 'Extra Tools', # Or 'Administration', 'Technical'
    'depends': ['base'], # Depends on the base Odoo module
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_setup_assistant_views.xml',
        # Add security CSV if specific groups beyond base.group_system are needed later
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'compatible_version': '18.0',
    # It's good practice to note external Python dependencies if your module *itself*
    # directly depends on something not standard in Odoo's core requirements.
    # For the 'packaging' library used by addon_requirements_checker.py,
    # it's often present with pip/setuptools. If it were less common, you might note it here.
    # 'external_dependencies': {'python': ['packaging']}, # Example
}