# 🛠️ ECOSIRE Setup Assistant

[![Odoo Version](https://img.shields.io/badge/Odoo-15,16,17+-%237C7BAD)](https://www.odoo.com)
[![License: OPL-1](https://img.shields.io/badge/License-OPL--1-blue.svg)](https://www.odoo.com/documentation/17.0/legal/licenses/licenses.html#odoo-proprietary-license-v1-0)
The **ECOSIRE Setup Assistant** is a comprehensive diagnostic and configuration toolkit designed to streamline the management and health-checking of your Odoo environments. Developed by Ecosire (PRIVATE) LIMITED, this module empowers developers, administrators, and consultants to ensure Odoo instances run smoothly and efficiently.

## Overview

Setting up and maintaining an Odoo environment can involve managing numerous dependencies, validating configurations, and troubleshooting elusive issues. The Odoo Setup Assistant simplifies these tasks by providing a centralized interface within Odoo to:

* Verify Python and system dependencies.
* Manage Python requirements for custom addons.
* Analyze database connectivity and health.
* Deep-scan `odoo.conf` for common issues and best practices.
* Inspect Odoo log files.
* Automate the installation of missing Python dependencies (requires server-side configuration).
* Facilitate Odoo service restarts directly from the UI (requires server-side configuration).
* Manage and update modules from configured GitHub repositories.

This module aims to reduce setup time, minimize errors, and provide insights for a more stable and performant Odoo instance.

## ✨ Key Features

* **🐍 Python & System Dependencies Check:** Automatically scans for required Python libraries (e.g., `num2words`, `phonenumbers`) and system-level executables (like `wkhtmltopdf`, `psql`), highlighting missing components.
* **📦 Addon Python Requirements Management:** Scans all custom and community addons for `requirements.txt` files. Lists missing Python packages and, with proper server configuration, allows for their installation.
* **💾 Database Health Analysis:** Verifies database connection parameters from `odoo.conf`, attempts direct PostgreSQL server connection, and checks Odoo's current database session.
* **⚙️ Odoo.conf Deep Scan:** Analyzes your `odoo.conf` file for critical path validations (`addons_path`, `data_dir`), performance settings (workers, limits), security configurations (`admin_passwd`, `list_db`), and common misconfigurations.
* **📄 Log File Analysis & Configuration:** Provides tools to fetch, filter (by level, keyword), and display recent log entries. Includes diagnostic hints for common errors. Allows setting a custom log file path for analysis.
* **🔗 GitHub Repository Management:** Configure GitHub repositories (public or private with Personal Access Tokens - PAT) to easily clone or pull module updates directly into your Odoo addons path from the interface.
* **🛠️ Automated Dependency Installation (Advanced):** Offers an action to attempt automatic installation of identified missing Python libraries directly from the Odoo interface. *Requires server-side `sudo` configuration.*
* **🔄 Odoo Service Restart (Advanced):** Provides a button to initiate a restart of the Odoo service. *Requires server-side `sudo` configuration.*
* **📊 User-Friendly Interface:** All checks and actions are available within a clean, tabbed Odoo interface.

## 📸 Screenshots

*(It's recommended to add a few key screenshots here or link to a gallery/Odoo App Store page if you have many)*

* **Example Screenshot 1:** Main dashboard showing overall system health.
    ```
    ```
* **Example Screenshot 2:** Dependency check results.
    ```
    ```
* **Example Screenshot 3:** Odoo.conf analysis.
    ```
    ```

## 🎯 Who is it for?

* **Odoo Developers:** For rapid environment validation and dependency management.
* **System Administrators:** For maintaining and troubleshooting Odoo instances.
* **Technical Consultants:** For provisioning or auditing client setups.
* **DevOps Teams:** For integrating Odoo environment checks into CI/CD pipelines.
* **Anyone** managing Odoo instances who wants a clearer view of their setup.

## 📂 Installation

1.  Clone this repository or download the `odoo_setup_assistant` module.
2.  Place the `odoo_setup_assistant` directory into your Odoo `addons` path.
3.  Restart your Odoo server.
4.  Navigate to 'Apps' in Odoo.
5.  Search for "Odoo Setup Assistant".
6.  Click 'Activate'.

## ⚙️ Configuration

### Basic Configuration

* **Log File Path (Optional):** Within the module's settings in Odoo, you can specify a custom path to your Odoo log file if it differs from the one in `odoo.conf` or if you want to analyze a specific log.
* **GitHub Repositories:**
    * Navigate to the Setup Assistant > GitHub Repositories section.
    * Add new repositories by providing a name, URL, target branch, and optionally a Personal Access Token (PAT) for private repositories. Ensure the PAT has the necessary scopes (e.g., `repo`).

### Advanced: Automated Dependency Installation & Service Restart

These features provide significant automation capabilities but require careful server-side configuration to grant the Odoo user permission to execute specific commands with `sudo`.

**⚠️ Security Warning:** Incorrect `sudo` configuration can expose your server to significant security risks. Proceed with caution and ensure you understand the implications. Only grant the minimum necessary permissions.

**Recommended Approach: Wrapper Scripts**

1.  **Create Wrapper Scripts:**
    Create shell scripts on your Odoo server that will perform the actual pip installations and service restarts. These scripts should include error handling and logging. **Crucially, the script for installing packages must validate/sanitize any package name input to prevent command injection.**

    * Example `install_odoo_library.sh` (place in e.g., `/opt/odoo_automation_scripts/`):
        ```bash
        #!/bin/bash
        set -e
        LOG_FILE="/var/log/odoo/automation_script.log" # Ensure odoo user can write or use sudo tee
        # IMPORTANT: Use pip from Odoo's virtualenv or ensure correct environment
        PYTHON_PIP_PATH="/opt/odoo/venv/bin/pip" # ADJUST THIS PATH
        PACKAGE_NAME="$1"

        # Basic input validation (enhance as needed)
        if [[ -z "$PACKAGE_NAME" ]] || ! [[ "$PACKAGE_NAME" =~ ^[a-zA-Z0-9._-]+([=><]{1,2}[a-zA-Z0-9._-]+)?$ ]]; then
            echo "$(date): ERROR - Invalid package name: $PACKAGE_NAME" | sudo tee -a "$LOG_FILE" >&2
            exit 1
        fi

        echo "$(date): INFO - Attempting to install: $PACKAGE_NAME" | sudo tee -a "$LOG_FILE"
        if sudo $PYTHON_PIP_PATH install "$PACKAGE_NAME"; then
            echo "$(date): SUCCESS - Installed $PACKAGE_NAME" | sudo tee -a "$LOG_FILE"
        else
            echo "$(date): ERROR - Failed to install $PACKAGE_NAME" | sudo tee -a "$LOG_FILE" >&2
            exit 1
        fi
        exit 0
        ```

    * Example `restart_odoo_service.sh` (place in e.g., `/opt/odoo_automation_scripts/`):
        ```bash
        #!/bin/bash
        set -e
        LOG_FILE="/var/log/odoo/automation_script.log"
        ODOO_SERVICE_NAME="odoo.service" # ADJUST THIS to your Odoo service name

        echo "$(date): INFO - Attempting to restart Odoo service: $ODOO_SERVICE_NAME" | sudo tee -a "$LOG_FILE"
        if sudo systemctl restart "$ODOO_SERVICE_NAME"; then
            echo "$(date): SUCCESS - Restarted $ODOO_SERVICE_NAME" | sudo tee -a "$LOG_FILE"
        else
            echo "$(date): ERROR - Failed to restart $ODOO_SERVICE_NAME" | sudo tee -a "$LOG_FILE" >&2
            exit 1
        fi
        exit 0
        ```
    * **Permissions:** Ensure these scripts are owned by `root` and are not writable by the Odoo user. E.g., `sudo chown root:root /opt/odoo_automation_scripts/*; sudo chmod 750 /opt/odoo_automation_scripts/*`.

2.  **Configure `sudoers`:**
    Run `sudo visudo` and add lines to allow the user Odoo runs as (e.g., `odoo` or `your_odoo_user`) to execute these specific scripts without a password:
    ```sudoers
    # Replace 'your_odoo_user' with the actual user Odoo runs as.
    your_odoo_user ALL=(ALL) NOPASSWD: /opt/odoo_automation_scripts/install_odoo_library.sh
    your_odoo_user ALL=(ALL) NOPASSWD: /opt/odoo_automation_scripts/restart_odoo_service.sh
    ```

3.  **Configure Script Paths in Odoo:**
    In the Odoo Setup Assistant settings within Odoo, you will find fields to specify the full paths to these configured wrapper scripts. The module will then use these paths when triggering the actions.

## 🚀 Usage

1.  Once installed, the "Setup Assistant" menu will appear in your Odoo dashboard or Apps list.
2.  Navigate through the different tabs to access various checks and tools:
    * **Dashboard:** Overview of checks.
    * **Dependencies:** View Python and System dependencies.
    * **Addon Requirements:** Manage Python packages for your addons. Click "Scan Addons" and then "Install Missing Packages" (if advanced configuration is done).
    * **Database:** Check database connectivity.
    * **Odoo Config:** Analyze `odoo.conf`.
    * **Logs:** View and filter Odoo logs.
    * **GitHub:** Manage addon repositories.
    * **Actions:** Find the "Restart Odoo Service" button (if advanced configuration is done).
    * **Settings:** Configure paths for advanced features.

## ⚠️ Important Security Note for Privileged Operations

The features for automated dependency installation and Odoo service restart interact with your server's system-level operations.
* **Only enable these features if you understand the security implications.**
* **Always use wrapper scripts as described above.** Do not grant direct `sudo` access to `pip` or `systemctl` for the Odoo user.
* **Regularly review your `sudoers` configuration and script permissions.**
* Ensure your Odoo instance itself is secured against unauthorized access.

The Odoo Setup Assistant module executes these configured scripts as is; the security of the scripts and the `sudo` configuration is the responsibility of the server administrator.

## 📌 Pro-Tips / Best Practices

* Regularly use the assistant after server updates, new module installations, or configuration changes.
* For the "Automated Dependency Installation," ensure the specified pip path in your wrapper script points to the correct Python environment for your Odoo instance (preferably a virtual environment).
* Integrate checks into your CI/CD pipeline by potentially scripting calls to the Odoo RPC to trigger specific analyses if needed (advanced usage).

## 🤝 How to Contribute (Optional)

We welcome contributions! If you have suggestions, bug reports, or want to contribute code:

1.  Please open an issue first to discuss what you would like to change.
2.  Fork the repository and create your feature branch.
3.  Commit your changes and open a pull request.

## 📞 Support & Contact

Developed by **Ecosire (PRIVATE) LIMITED**.
* AI Automation, ERP Solutions, and Growth Technologies.
* Website: [https://www.ecosire.com](https://www.ecosire.com)
* For direct support or inquiries: Contact us on [WhatsApp](https://wa.me/923130168262) or open an issue on GitHub.

## 📜 License

This module is distributed under the OPL-1 (Odoo Proprietary License v1.0).
See the `LICENSE` file in this repository or [Odoo Licensing](https://www.odoo.com/documentation/17.0/legal/licenses/licenses.html#odoo-proprietary-license-v1-0).
*(Please replace with your chosen license, e.g., AGPL-3, MIT, if OPL-1 is not your intention for a public GitHub repo. If it's a private repo for a client, OPL-1 is common).*

## 📢 Disclaimer

This module is provided "as is", without warranty of any kind. The developers assume no liability for any issues, damages, or security breaches that may arise from its use, especially concerning features that require server-level `sudo` configurations. You are solely responsible for the security and stability of your server environment. Always test thoroughly in a staging environment before deploying to production.
