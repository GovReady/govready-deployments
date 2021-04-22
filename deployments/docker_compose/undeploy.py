from utils.deployment import UnDeploy
from utils.prompts import Prompt, Colors


class DockerComposeRemoveDeployment(UnDeploy):

    def on_fail(self):
        pass

    def on_sig_kill(self):
        pass

    def on_complete(self):
        print()
        Prompt.warning(f"If you're not using an external database and would like to wipe your DB, run: {Colors.CYAN}docker volume rm govready-q_postgres-data")

    def run(self):
        self.check_if_docker_is_started()
        self.execute(cmd="docker-compose down --remove-orphans")

