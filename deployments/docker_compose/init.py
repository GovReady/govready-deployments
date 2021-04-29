from utils.deployment import Initialize
from utils.prompts import Prompt, Colors


class DockerComposeInit(Initialize):
    def on_sig_kill(self):
        pass

    def on_complete(self):
        Prompt.notice(f"Next step: {Colors.CYAN}python run.py deploy --type docker-compose --config configuration.json")

    def on_fail(self):
        pass

    def run(self, config):
        config['SECRET_KEY'] = self.create_secret()
        config['REMOVE_STACK_ON_FAIL'] = True
