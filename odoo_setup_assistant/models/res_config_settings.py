# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    setup_assist_base_git_dir = fields.Char(
        string='Base Git Cloning Directory',
        config_parameter='setup.assist.base_git_dir',
        help='Base directory where GitHub repositories will be cloned by the Setup Assistant.'
    ) 