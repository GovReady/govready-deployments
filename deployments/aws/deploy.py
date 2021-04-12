import os

from build_utils.deployment import Deployment


class AWSDeployment(Deployment):

    def on_complete(self):
        pass

    def on_sig_kill(self):
        pass

    def run(self):
        pass
