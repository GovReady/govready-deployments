from utils.deployment import Deployment


class AzureDeployment(Deployment):

    def on_sig_kill(self):
        pass

    def on_complete(self):
        pass

    def on_fail(self):
        pass

    def run(self):
        pass
