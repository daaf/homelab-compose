#!/usr/bin/sudo /usr/bin/env python

from os import listdir, path
from decouple import config
from subprocess import run
from utils import bytes_to_ascii_list, create_dir_if_not_extant

STACKS = {
    'network-stack': ['duckdns', 'pihole-unbound'],
    'grafana-stack': ['telegraf', 'influxdb', 'chronograf',  'grafana'],
    'heimdall-stack': ['heimdall'],
    'home-stack': ['grocy'],
    'rss-stack': ['freshrss', 'mariadb']
}


def get_compose_attribute_value(compose_file, keyword):
    with open(compose_file) as file:
        for line in file:
            if keyword in line:
                value = line.replace(f'{keyword}:', '').strip()
                return value


def get_stack_name_from_app_name(app):
    for stack in STACKS:
        if app in STACKS[stack]:
            return stack


def print_output(output):
    for stdout, stderr in output:
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)


def link_compose_file(dir, compose_file):
    output = []
    link_path = f'{dir}/docker-compose.yml'

    if not path.exists(link_path):
        process = run([
            'sudo',
            'ln',
            compose_file,
            link_path
        ], capture_output=True)
        process_output = bytes_to_ascii_list(process.stdout, process.stderr)
        output.append(process_output)

    return output


def link_compose_files(portainer_compose_dir, linked_dir):
    for subdir in listdir(portainer_compose_dir):
        compose_file = f'{portainer_compose_dir}/{subdir}/docker-compose.yml'
        app_name = get_compose_attribute_value(compose_file, 'container_name')
        stack_name = get_stack_name_from_app_name(app_name)
        stack_dir = f'{linked_dir}/{stack_name}'
        create_dir_if_not_extant(stack_dir)

        # Link the Compose files and assign the resulting stdout and stderr to `output`
        output = link_compose_file(stack_dir, compose_file)
        print_output(output)


if __name__ == "__main__":
    portainer_compose_dir = config('PORTAINER_COMPOSE_DIR')
    local_repo = config('HOMELAB_COMPOSE_REPO')
    link_compose_files(portainer_compose_dir, local_repo)
