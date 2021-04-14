import os

from build_utils.deployment import Deployment


class OnPremiseSimpleDeployment(Deployment):
    TMP_BUILD_FILES = [
        {"image": 'nginx', "keys": ['NGINX_CERT', 'NGINX_KEY']},
        {"image": 'govready-q', "keys": ['BRANDING']},
    ]
    REQUIRED_PORTS = [80, 8000, 443, 5432]

    def on_fail(self):
        self.execute(cmd=f"docker-compose logs")
        self.on_sig_kill()

    def on_complete(self):
        self.execute(cmd=f"docker-compose logs")

    def on_sig_kill(self):
        self.execute(cmd="docker-compose down --remove-orphans  --rmi all")

    def run(self):
        self.set_default('GIT_URL', "https://github.com/GovReady/govready-q.git")
        self.set_default('ADMINS', [] if not self.config.get('ADMINS') else self.config.get('ADMINS'))
        self.set_default('MOUNT_FOLDER', os.path.abspath("../../volumes"))
        self.set_default('HTTPS', "true")
        self.set_default('DEBUG', "false")
        self.set_default('HOST', self.config['ADDRESS'].split(':')[0])
        self.set_default('HEALTH_CHECK_GOVREADY_Q', f"http://{self.config['HOST']}:8000")
        using_internal_db = self.set_default('DATABASE_CONNECTION_STRING',
                                             "postgres://postgres:PASSWORD@postgres:5432/govready_q")
        docker_compose_file = "docker-compose.yaml"
        if not using_internal_db:
            docker_compose_file = 'docker-compose.external-db.yaml'

        self.execute(cmd=f"docker-compose -f {docker_compose_file} down --remove-orphans  --rmi all")
        self.check_ports()
        self.execute(cmd=f"docker-compose -f {docker_compose_file} build", show_env=True)
        self.execute(cmd=f"docker-compose -f {docker_compose_file} up -d", show_env=True)
