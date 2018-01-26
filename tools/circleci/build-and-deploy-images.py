import yaml

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

with open("Dockerfile.template") as f:
    docker_template = f.read()

with open("images.yml") as f:
    custom_settings = yaml.safe_load(f)

xenial_docker_image = docker_template.format_map(SafeDict(custom_settings["xenial"]))
with open("images/xenial/Dockerfile", "w") as f:
    f.write(xenial_docker_image)
