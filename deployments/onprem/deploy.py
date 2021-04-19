import os
import re
from build_utils.deployment import Deployment
from build_utils.prompts import Prompt, Colors


class OnPremiseDeployment(Deployment):
    TMP_BUILD_FILES = [
        {"image": 'nginx', "keys": ['NGINX_CERT', 'NGINX_KEY']},
        {"image": 'govready-q', "keys": ['BRANDING']},
    ]
    REQUIRED_PORTS = [80, 8000, 443, 5432]

    def on_fail(self):
        self.execute(cmd=f"docker-compose logs")
        self.on_sig_kill()

    def on_complete(self):
        logs = self.execute(cmd=f"docker-compose logs", display_stdout=False)
        auto_admin = re.findall('Created administrator account \(username: (admin)\) with password: ([a-zA-Z0-9#?!@$%^&*-]+)', logs)
        print()

        if auto_admin:
            Prompt.warning(f"Created Administrator Account - {Colors.CYAN}{auto_admin[0][0]} / {auto_admin[0][1]} - {Colors.FAIL} This is the only time you will see this message so make sure to write this down!")
        Prompt.warning(f"Logs & Container Artifacts can be found in: {Colors.CYAN}{self.config['MOUNT_FOLDER']}")
        Prompt.warning(f"Access application via Browser: {Colors.CYAN}https://{self.config['HOST']}")

    def on_sig_kill(self):
        self.execute(cmd="docker-compose down --remove-orphans  --rmi all")

    def run(self):
        self.set_default('GIT_URL', "https://github.com/GovReady/govready-q.git")
        self.set_default('ADMINS', [] if not self.config.get('ADMINS') else self.config.get('ADMINS'))
        self.set_default('MOUNT_FOLDER', os.path.abspath("../../volumes"))
        self.set_default('HTTPS', "true")
        self.set_default('DEBUG', "false")

        if self.check_if_valid_uri(self.config['ADDRESS']):
            Prompt.error(f"ADDRESS cannot be a valid URI.  It must be the <domain>:<port> only.  No protocol or path.  "
                         f"{self.config['ADDRESS']} is invalid.", close=True)

        self.set_default('HOST', self.config['ADDRESS'].split(':')[0])
        self.set_default('HEALTH_CHECK_GOVREADY_Q', f"http://{self.config['HOST']}:8000")

        using_internal_db = self.set_default('DATABASE_CONNECTION_STRING',
                                             "postgres://postgres:PASSWORD@postgres:5432/govready_q")
        self.set_default('DB_ENGINE', self.config['DATABASE_CONNECTION_STRING'].split(':')[0])
        docker_compose_file = "docker-compose.yaml"
        if not using_internal_db:
            docker_compose_file = 'docker-compose.external-db.yaml'

        self.execute(cmd=f"docker-compose -f {docker_compose_file} down --remove-orphans  --rmi all")
        self.check_ports()
        self.execute(cmd=f"docker-compose -f {docker_compose_file} build --parallel", show_env=True)
        self.execute(cmd=f"docker-compose -f {docker_compose_file} up -d", show_env=True)
