import sys
import subprocess
import platform
import os
from odoo import models, api, _
from odoo.exceptions import UserError

class DependencyInstaller(models.TransientModel):
    _name = 'setup.assistant.dependency.installer'
    _description = 'Setup Assistant Dependency Installer'

    def _get_current_user(self):
        try:
            return os.getlogin()
        except Exception:
            return str(os.geteuid())

    @api.model
    def install_python_packages(self, packages):
        results = {}
        user = self._get_current_user()
        for pkg in packages:
            try:
                cmd = [sys.executable, '-m', 'pip', 'install', pkg]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    results[pkg] = {'success': True, 'log': result.stdout, 'user': user}
                else:
                    results[pkg] = {'success': False, 'log': result.stderr, 'user': user}
            except Exception as e:
                results[pkg] = {'success': False, 'log': str(e), 'user': user}
        return results

    @api.model
    def install_system_packages(self, packages):
        os_type = platform.system().lower()
        results = {}
        user = self._get_current_user()
        for pkg in packages:
            try:
                if os_type == 'windows':
                    cmd = ['choco', 'install', pkg, '-y']
                elif os_type == 'linux':
                    if subprocess.call(['which', 'apt-get']) == 0:
                        cmd = ['apt-get', 'install', '-y', pkg]
                    elif subprocess.call(['which', 'yum']) == 0:
                        cmd = ['yum', 'install', '-y', pkg]
                    else:
                        raise UserError(_('No supported package manager found.'))
                else:
                    raise UserError(_('Unsupported OS for system package installation.'))

                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    results[pkg] = {'success': True, 'log': result.stdout, 'user': user}
                else:
                    results[pkg] = {'success': False, 'log': result.stderr, 'user': user}
            except Exception as e:
                results[pkg] = {'success': False, 'log': str(e), 'user': user}
        return results

    @api.model
    def install_all(self, python_packages, system_packages):
        py_result = self.install_python_packages(python_packages)
        sys_result = self.install_system_packages(system_packages)
        return {'python': py_result, 'system': sys_result, 'user': self._get_current_user()}

    @api.model
    def restart_odoo_service(self):
        import shutil
        import time
        user = self._get_current_user()
        commands_tried = []
        try:
            # Try systemctl
            if shutil.which('systemctl'):
                cmd = ['systemctl', 'restart', 'odoo']
                commands_tried.append(' '.join(cmd))
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return {'success': True, 'log': 'Odoo service restarted using systemctl.', 'user': user}
                else:
                    return {'success': False, 'log': result.stderr, 'user': user, 'commands_tried': commands_tried}
            # Try service
            elif shutil.which('service'):
                cmd = ['service', 'odoo', 'restart']
                commands_tried.append(' '.join(cmd))
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return {'success': True, 'log': 'Odoo service restarted using service.', 'user': user}
                else:
                    return {'success': False, 'log': result.stderr, 'user': user, 'commands_tried': commands_tried}
            # Try supervisorctl
            elif shutil.which('supervisorctl'):
                cmd = ['supervisorctl', 'restart', 'odoo']
                commands_tried.append(' '.join(cmd))
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return {'success': True, 'log': 'Odoo service restarted using supervisorctl.', 'user': user}
                else:
                    return {'success': False, 'log': result.stderr, 'user': user, 'commands_tried': commands_tried}
            else:
                return {'success': False, 'log': 'No known service manager found (systemctl, service, supervisorctl).', 'user': user, 'commands_tried': commands_tried}
        except Exception as e:
            return {'success': False, 'log': str(e), 'user': user, 'commands_tried': commands_tried} 