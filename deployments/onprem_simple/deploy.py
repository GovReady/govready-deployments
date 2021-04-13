import os

from build_utils.deployment import Deployment


class OnPremiseSimpleDeployment(Deployment):

    TMP_BUILD_FILES = [{"image": 'nginx', "keys": ['NGINX_CERT', 'NGINX_KEY']}]

    def on_fail(self):
        self.execute(cmd=f"docker-compose logs")
        self.on_sig_kill()

    def on_complete(self):
        self.docker_build_tmp_files_cleanup(self.TMP_BUILD_FILES)
        self.execute(cmd=f"docker-compose logs")

    def on_sig_kill(self):
        self.docker_build_tmp_files_cleanup(self.TMP_BUILD_FILES)
        self.execute(cmd="docker-compose down --remove-orphans  --rmi all")

    def run(self):
        self.set_default('GIT_URL', "https://github.com/GovReady/govready-q.git")
        latest_version = self.execute(cmd=f"git -c versionsort.suffix=- ls-remote --tags --sort=v:refname {self.config['GIT_URL']}",
                                      display_stdout=False)[-1].split("/")[-1]
        self.set_default('VERSION', latest_version)
        self.set_default('ADMINS', self.config.get('ADMINS', []))
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

        self.docker_build_tmp_files_copy(self.TMP_BUILD_FILES)
        self.execute(cmd=f"docker-compose -f {docker_compose_file} build", show_env=True)
        self.execute(cmd=f"docker-compose -f {docker_compose_file} up -d", show_env=True)
