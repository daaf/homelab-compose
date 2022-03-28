#!/usr/bin/sudo /usr/bin/env python

import utils
from os import listdir, mkdir, link, path
from decouple import config

STACKS = {
    'network-stack': ['duckdns', 'pihole-unbound'],
    'grafana-stack': ['telegraf', 'influxdb', 'chronograf',  'grafana'],
    'heimdall-stack': ['heimdall'],
    'home-stack': ['grocy'],
    'rss-stack': ['freshrss', 'mariadb'],
    'test-stack': ['alpine']
}


def get_stack_name_from_app_name(app):
    """Search the STACKS dictionary for `app`. If `app` is found, 
    return the name of the stack."""
    for stack in STACKS:
        if app in STACKS[stack]:
            return stack


def link_compose_files(portainer_compose_dir, linked_dir):
    """
    Iterate through the Docker Compose files in Portainer's data directory.
    For each Compose file, create a subdirectory with the stack name in a 
    second directory and, inside each stack directory, create links to the 
    corresponding Compose file in Portainer's data directory.

    :param portainer_compose_dir: The path to the `compose` directory inside 
        Portainer's data directory.
    :param linked_dir: The directory in which to create the links.
    """
    for subdir in listdir(portainer_compose_dir):
        path_to_compose_file = f'{portainer_compose_dir}/{subdir}/docker-compose.yml'
        app_name = utils.get_compose_attribute_value(
            path_to_compose_file, 'container_name')
        stack_name = get_stack_name_from_app_name(app_name)
        path_to_stack_dir = f'{linked_dir}/{stack_name}'

        if not path.exists(path_to_stack_dir):
            mkdir(path_to_stack_dir)

        path_to_link = f'{path_to_stack_dir}/docker-compose.yml'

        if not path.exists(path_to_link):
            link(path_to_compose_file, path_to_link)


if __name__ == '__main__':
    portainer_compose_dir = config('PORTAINER_COMPOSE_DIR')
    local_repo = config('HOMELAB_COMPOSE_REPO')
    link_compose_files(portainer_compose_dir, local_repo)
