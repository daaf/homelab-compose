#!/usr/bin/env python3

# Standard library imports
from os import listdir, mkdir, link, path

# Local imports
from dockerutils import get_compose_attribute_value

STACKS = {
    "network-stack": ["duckdns", "pihole-unbound"],
    "grafana-stack": ["telegraf", "influxdb", "chronograf", "grafana"],
    "heimdall-stack": ["heimdall"],
    "home-stack": ["grocy"],
    "rss-stack": ["freshrss", "mariadb"],
    "test-stack": ["alpine"],
}


def get_stack_name_from_app_name(app):
    """Search the STACKS dictionary for `app`. If `app` is found,
    return the name of the stack."""
    for stack in STACKS:
        if app in STACKS[stack]:
            return stack


def link(portainer_compose_dir, linked_dir):
    """
    Iterate through the Docker Compose files in Portainer's data directory.
    For each Compose file, in a second directory, create a subdirectory with
    the same name as the stack. Inside the stack directory, create a link to the
    corresponding Compose file in Portainer's data directory.

    :param portainer_compose_dir: The path to the `compose` directory inside
        Portainer's data directory.
    :param linked_dir: The directory in which to create the links.
    """
    new_link_count = 0

    for subdir in listdir(portainer_compose_dir):
        path_to_compose_file = f"{portainer_compose_dir}/{subdir}/docker-compose.yml"
        app_name = get_compose_attribute_value(path_to_compose_file, "container_name")
        stack_name = get_stack_name_from_app_name(app_name)
        path_to_stack_dir = f"{linked_dir}/{stack_name}"

        print()
        print(f"Checking for link to docker-compose.yml for {stack_name}...")

        if not path.exists(path_to_stack_dir):
            mkdir(path_to_stack_dir)
            print(f"\tCreated {path_to_stack_dir}")
        else:
            print(f"\t{path_to_stack_dir} already exists.")

        path_to_link = f"{path_to_stack_dir}/docker-compose.yml"

        if not path.exists(path_to_link):
            new_link_count += 1
            link(path_to_compose_file, path_to_link)
            print(f"\tAdded link to {path_to_compose_file} in {path_to_link}.")
        else:
            print(f"\t{path_to_link} already exists.")

        print()

    if new_link_count > 1:
        print(f"Created {new_link_count} new links to Compose files.")
    elif new_link_count > 0:
        print(f"Created 1 new link to Compose file.")
    else:
        print("Nothing to update.")

    print()
