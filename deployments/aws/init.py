from utils.deployment import Initialize


class AWSInit(Initialize):
    def on_sig_kill(self):
        pass

    def on_complete(self):
        pass

    def on_fail(self):
        pass

    def run(self, config):
        config['SECRET_KEY'] = self.create_secret()
