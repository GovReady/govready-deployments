import os

from build_utils.deployment import Deployment


class OnPremiseSimpleDeployment(Deployment):

    def on_complete(self):
        pass

    def on_sig_kill(self):
        self.execute(cmd="docker-compose down --remove-orphans", env_dict={})

    def run(self):
        self.set_default('GIT_URL', "https://github.com/GovReady/govready-q.git")
        latest_version = self.execute(cmd=f"git -c versionsort.suffix=- ls-remote --tags --sort=v:refname {self.config['GIT_URL']}",
                                      env_dict={},
                                      display_stdout=False)[-1].split("/")[-1]

        self.set_default('VERSION', latest_version)
        self.set_default('ADMINS', self.config.get('ADMINS', []))
        self.set_default('MOUNT_FOLDER', os.path.abspath("../../volumes"))
        self.set_default('HTTPS', "true")
        self.set_default('DEBUG', "false")
        using_internal_db = self.set_default('DATABASE_CONNECTION_STRING',
                                             "postgres://postgres:PASSWORD@postgres:5432/govready_q")
        docker_compose_file = "docker-compose.yaml"
        if not using_internal_db:
            docker_compose_file = 'docker-compose.external-db.yaml'

        self.execute(cmd=f"docker-compose -f {docker_compose_file} down --remove-orphans", env_dict=self.config)
        self.execute(cmd=f"docker-compose -f {docker_compose_file} build", env_dict=self.config)
        self.execute(cmd=f"docker-compose -f {docker_compose_file} up -d", env_dict=self.config)

