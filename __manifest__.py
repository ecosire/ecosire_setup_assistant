# -*- coding: utf-8 -*-
{
    'name': 'Odoo Setup Assistant',
    'version': '1.1', # Incremented version for new features
    'summary': 'Diagnose Odoo setup, configuration, dependencies, and manage addon Python requirements.',
    'description': """
This module provides a comprehensive toolkit to:
- Check for missing Python libraries and system dependencies.
- Analyze Odoo database connectivity and configuration.
- Perform a deep scan of the odoo.conf file for best practices and common issues.
- Scan Odoo addons for their Python dependencies (requirements.txt) and allow automatic installation of missing packages.
Helps ensure your Odoo environment is correctly set up for optimal performance and stability.
    """,
    'author': 'ECOSIRE (PRIVATE) LIMITED',
    'website': 'https://www.ecosire.com/',
    'category': 'Extra Tools', # Or 'Administration', 'Technical'
    'depends': ['base'], # Depends on the base Odoo module
    'data': [
        'views/setup_assist_views.xml',
        # Add security CSV if specific groups beyond base.group_system are needed later
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    # It's good practice to note external Python dependencies if your module *itself*
    # directly depends on something not standard in Odoo's core requirements.
    # For the 'packaging' library used by addon_requirements_checker.py,
    # it's often present with pip/setuptools. If it were less common, you might note it here.
    # 'external_dependencies': {'python': ['packaging']}, # Example
}