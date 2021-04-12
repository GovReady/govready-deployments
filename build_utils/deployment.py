import json
import os
import signal
import subprocess
import sys
from abc import ABC

from build_utils.prompts import Prompt, Colors


class Helper:
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.kill_captured = False

    def execute(self, cmd, env_dict, display_stdout=True):
        env = os.environ.copy()
        normalized_dict = {}
        for key, value in env_dict.items():
            if isinstance(value, (list, dict)):
                value = json.dumps(value)
            if value is None:
                value = ""
            normalized_dict[key] = value
        env.update(normalized_dict)
        output = []
        Prompt.notice(f"Executing command: [{cmd}]")
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,  # stderr=subprocess.STDOUT,
                              bufsize=0, env=env) as proc:
            for line in proc.stdout:
                formatted = line.rstrip().decode()
                output.append(formatted)
                if display_stdout:
                    print(formatted)
        if proc.returncode != 0:
            Prompt.error(f"[{cmd}] Failed [code:{proc.returncode}]- {proc.stderr}", close=True)
        return output

    def signal_handler(self, sig, frame):
        Prompt.notice("\nCtrl-c captured.  Executing teardown function.")
        if not self.kill_captured:
            self.kill_captured = True
            self.on_sig_kill()
        sys.exit(0)

    def on_sig_kill(self):
        raise NotImplementedError()

    def on_complete(self):
        raise NotImplementedError()


class Deployment(Helper, ABC):
    def __init__(self, options, validator_json_file):
        super().__init__()
        self.options = options
        self.config = {}
        with open(validator_json_file, 'r') as f:
            self.validation_config = json.load(f)

    def set_default(self, variable, default):
        # Sets default to an optional field in the config OR creates a new entry if doesn't exist
        # Returns True if default was set else False
        if not self.config.get(variable):
            self.config[variable] = default
            return True
        return False

    def validate(self):
        with open(self.options['config'], 'r') as f:
            self.config = json.load(f)

        missing = []
        for item in self.validation_config:
            if item['key'] not in self.config and item['required']:
                missing.append(item)
            elif (item['key'] not in self.config and not item['required']) or (
                    not self.config.get(item['key']) and not item['required']):
                self.config[item['key']] = os.environ.get(item['key'])
                warning = f"Config missing optional field: [{item['key']}] - {Colors.WARNING}{item['description']}"
                if item.get('default-message'):
                    warning += f" - {Colors.CYAN}{item['default-message']}"
                Prompt.notice(warning)
        if missing:
            missing_formatted = [f"{x['key']}: {x['description']}]" for x in missing]
            Prompt.error(f"The following keys are missing from your config file: {missing_formatted}", close=True)

    def run(self):
        raise NotImplementedError()


class UnDeploy(Helper, ABC):

    def __init__(self, options):
        super().__init__()
        self.options = options

    def run(self):
        raise NotImplementedError()
