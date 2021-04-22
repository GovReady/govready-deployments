from utils.deployment import UnDeploy


class AzureRemoveDeployment(UnDeploy):

    def on_fail(self):
        pass

    def on_sig_kill(self):
        pass

    def on_complete(self):
        pass

    def run(self):
        pass

