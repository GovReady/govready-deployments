import json
import os
import signal
import subprocess
import sys
from abc import ABC
from contextlib import closing
from shutil import copyfile
from build_utils.prompts import Prompt, Colors


class Helper:
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.kill_captured = False

    def execute(self, cmd, env_dict, display_stdout=True, on_error_fn=None, show_env=False):
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
        Prompt.notice(f"Executing command: {Colors.WARNING}{cmd}")
        if show_env:
            Prompt.notice(f"Environment Variables: {json.dumps(env_dict, indent=4, sort_keys=True)}")
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,  # stderr=subprocess.STDOUT,
                              bufsize=0, env=env) as proc:
            for line in proc.stdout:
                formatted = line.rstrip().decode()
                output.append(formatted)
                if display_stdout:
                    print(formatted)
        if proc.returncode != 0:
            if on_error_fn:
                on_error_fn()
            Prompt.error(f"[{cmd}] Failed [code:{proc.returncode}]- {proc.stderr}", close=True)
        return output

    def signal_handler(self, sig, frame):
        Prompt.notice("\nCtrl-c captured.  Executing teardown function.")
        if not self.kill_captured:
            self.kill_captured = True
            self.on_sig_kill()
        sys.exit(0)

    def docker_build_tmp_files_copy(self, docker_tmp_build_files):
        for tmp_build in docker_tmp_build_files:
            for key in tmp_build['keys']:
                file_path = self.config[key]
                if file_path:
                    if not os.path.exists(file_path):
                        Prompt.error(f"{os.path.abspath(file_path)} does not exist.", close=True)
                    dest = os.path.join(self.config['ROOT_DIR'], 'images',
                                        tmp_build['image'], os.path.basename(file_path))
                    copyfile(file_path, dest)
                    self.config[f"BUILD_FILE_{key}"] = os.path.basename(dest)
                    Prompt.notice(f"Copied build file for image: {tmp_build['image']} - {dest}")

    def docker_build_tmp_files_cleanup(self, docker_tmp_build_files):
        for tmp_build in docker_tmp_build_files:
            for key in tmp_build['keys']:
                file_path = self.config[key]
                if file_path:
                    if not os.path.exists(file_path):
                        Prompt.error(f"{os.path.abspath(file_path)} does not exist.", close=True)
                    dest = os.path.join(self.config['ROOT_DIR'], 'images',
                                        tmp_build['image'], os.path.basename(file_path))
                    os.remove(dest)
                    Prompt.notice(f"Removed build file for image: {tmp_build['image']} - {dest}")

    def on_sig_kill(self):
        raise NotImplementedError()

    def on_complete(self):
        raise NotImplementedError()

    def on_fail(self):
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

    def execute(self, cmd, env_dict=None, display_stdout=True, on_error_fn=None, show_env=False):
        return super().execute(cmd,
                               display_stdout=display_stdout,
                               env_dict=env_dict if env_dict else self.config,
                               on_error_fn=self.on_fail, show_env=show_env)

    def validate(self):
        with open(self.options['config'], 'r') as f:
            self.config = json.load(f)
        self.config['ROOT_DIR'] = os.getcwd()
        missing = []
        for item in self.validation_config:
            if (item['key'] not in self.config and item['required']) or \
                    (not self.config.get(item['key']) and item['required']):
                missing.append(item)
            elif (item['key'] not in self.config and not item['required']) or (
                    not self.config.get(item['key']) and not item['required']):
                self.config[item['key']] = os.environ.get(item['key'])
                if not self.config[item['key']]:
                    self.config[item['key']] = ""
                warning = f"Config missing optional field: {item['key']} - {Colors.WARNING}{item['description']}"
                if item.get('default-message'):
                    warning += f" - {Colors.CYAN}{item['default-message']}"
                Prompt.notice(warning)
        if missing:
            missing_formatted = [f"{x['key']}: {x['description']}" for x in missing]
            Prompt.error(f"The following keys are missing from your config file: {missing_formatted}", close=True)

    def check_ports(self, ports):
        Prompt.notice(f"Checking if ports are available for deployment: {ports}")
        import socket
        ports_in_use = []
        for port in ports:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                if sock.connect_ex(('127.0.0.1', port)) == 0:
                    ports_in_use.append(port)
        if ports_in_use:
            Prompt.error(f"Cannot deploy.  The following ports are in use: {ports_in_use}", close=True)

    def run(self):
        raise NotImplementedError()


class UnDeploy(Helper, ABC):

    def __init__(self, options):
        super().__init__()
        self.options = options

    def run(self):
        raise NotImplementedError()

    def execute(self, cmd, env_dict=None, display_stdout=True, on_error_fn=None, show_env=False):
        return super().execute(cmd, env_dict, display_stdout, on_error_fn=self.on_fail, show_env=show_env)
