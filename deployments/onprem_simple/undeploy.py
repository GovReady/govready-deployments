from build_utils.deployment import UnDeploy


class OnPremiseSimpleRemoveDeployment(UnDeploy):

    def on_sig_kill(self):
        pass

    def on_complete(self):
        pass

    def run(self):
        self.execute(cmd="docker-compose down --remove-orphans", env_dict={})

