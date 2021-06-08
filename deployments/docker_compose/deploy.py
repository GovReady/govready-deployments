import os
import re
from utils.deployment import Deployment
from utils.prompts import Prompt, Colors


class DockerComposeDeployment(Deployment):
    TMP_BUILD_FILES = [
        {"image": 'nginx', "keys": ['NGINX_CERT', 'NGINX_KEY']},
        {"image": 'govready-q', "keys": ['BRANDING']},
    ]
    REQUIRED_PORTS = [5432]

    FAIL_SUFFIX = ""

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

        url = f"https://{self.config['HOST_ADDRESS']}"
        if self.config['HOST_PORT_HTTPS']:
            url += f":{self.config['HOST_PORT_HTTPS']}"
        Prompt.warning(f"Access application via Browser: {Colors.CYAN}{url}")

    def on_sig_kill(self):
        self.execute(cmd=f"docker-compose down {self.FAIL_SUFFIX}")

    def run(self):
        self.config.setdefault('REMOVE_STACK_ON_FAIL')
        if self.config['REMOVE_STACK_ON_FAIL']:
            self.FAIL_SUFFIX = "--remove-orphans --rmi all"
        del self.config['REMOVE_STACK_ON_FAIL']

        self.check_if_docker_is_started()
        self.set_default('COMPOSE_PROJECT_NAME', 'govready-q')  # Prefix for all docker containers

        self.set_default('GIT_URL', "https://github.com/GovReady/govready-q.git")
        self.set_default('ADMINS', [] if not self.config.get('ADMINS') else self.config.get('ADMINS'))
        self.set_default('MOUNT_FOLDER', os.path.abspath("../../volumes"))
        self.set_default('DEBUG', "false")
        self.set_default('APP_DOCKER_PORT', "18000")

        if self.check_if_valid_uri(self.config['HOST_ADDRESS']):
            Prompt.error(f"HOST_ADDRESS cannot be a valid URI.  It must be the domain only.  "
                         f"No protocol or path.  {self.config['HOST_ADDRESS']} is invalid.", close=True)

        self.set_default('HEALTH_CHECK_GOVREADY_Q', f"http://app:{self.config['APP_DOCKER_PORT']}")
        using_internal_db = self.set_default('DATABASE_CONNECTION_STRING',
                                             "postgres://postgres:PASSWORD@postgres:5432/govready_q")
        self.set_default('DB_ENGINE', self.config['DATABASE_CONNECTION_STRING'].split(':')[0])
        docker_compose_file = "docker-compose.yaml"
        if not using_internal_db:
            docker_compose_file = 'docker-compose.external-db.yaml'

        self.execute(cmd=f"docker-compose -f {docker_compose_file} down {self.FAIL_SUFFIX}")

        self.REQUIRED_PORTS += [int(self.config['HOST_PORT_HTTPS']),
                                int(self.config['APP_DOCKER_PORT'])
                                ]
        self.check_ports()
        self.execute(cmd=f"docker-compose -f {docker_compose_file} build --parallel --no-cache", show_env=True)
        self.execute(cmd=f"docker-compose -f {docker_compose_file} up -d", show_env=True)
