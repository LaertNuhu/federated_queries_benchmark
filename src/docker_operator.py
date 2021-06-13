import subprocess


class Operator:
    def run(self, command):
        return subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE
        ).stdout.read()


class DockerOperator(Operator):
    def __init__(self) -> None:
        pass

    def start_resource(self, resource):
        return self.run(f"docker-compose -f {resource} up -d")

    def stop_resource(self, resource):
        return self.run(f"docker-compose -f {resource} down")

    def execute(self, command):
        return self.run(f"docker {command}")
