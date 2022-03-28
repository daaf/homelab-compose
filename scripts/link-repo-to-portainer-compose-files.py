#!/usr/bin/sudo /usr/bin/env python

import utils
from os import listdir
from decouple import config

STACKS = {
    'network-stack': ['duckdns', 'pihole-unbound'],
    'grafana-stack': ['telegraf', 'influxdb', 'chronograf',  'grafana'],
    'heimdall-stack': ['heimdall'],
    'home-stack': ['grocy'],
    'rss-stack': ['freshrss', 'mariadb']
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
        stack_dir = f'{linked_dir}/{stack_name}'
        utils.create_dir_if_not_extant(stack_dir)
        path_to_link = f'{stack_dir}/docker-compose.yml'

        # Link the Compose files and assign the resulting stdout and stderr to `output`
        ln_output = utils.ln(path_to_compose_file, path_to_link)
        utils.print_process_output(ln_output)


if __name__ == "__main__":
    portainer_compose_dir = config('PORTAINER_COMPOSE_DIR')
    local_repo = config('HOMELAB_COMPOSE_REPO')
    link_compose_files(portainer_compose_dir, local_repo)
