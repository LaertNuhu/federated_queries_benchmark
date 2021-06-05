import subprocess


class DockerOperator:
    def __init__(self) -> None:
        pass

    def start_resource(self, resource):
        return subprocess.Popen(
            f"docker-compose -f {resource} up -d", shell=True, stdout=subprocess.PIPE
        ).stdout.read()

    def stop_resource(self, resource):
        return subprocess.Popen(
            f"docker-compose -f {resource} down", shell=True, stdout=subprocess.PIPE
        ).stdout.read()

    def execute(self, command):
        return subprocess.Popen(
            f"docker {command}", shell=True, stdout=subprocess.PIPE
        ).stdout.read()
