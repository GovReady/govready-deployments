from build_utils.deployment import UnDeploy
from build_utils.prompts import Prompt, Colors


class OnPremiseRemoveDeployment(UnDeploy):

    def on_fail(self):
        pass

    def on_sig_kill(self):
        pass

    def on_complete(self):
        print()
        Prompt.warning(f"If you're not using an external database and would like to wipe your DB, run: {Colors.CYAN}docker volume rm onprem_pg-data")

    def run(self):
        self.execute(cmd="docker-compose down --remove-orphans")

