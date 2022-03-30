#!/usr/bin/env python
"""
Create links to Portainer's Docker Compose files in a specified directory.

Usage:
    hc link

Options:
    -h --help   Show this help documentation.
"""

from docopt import docopt
from decouple import config
from hc import link_portainer_compose_files


def init():
    args = docopt(__doc__, version='0.1')
    portainer_compose_dir = config('PORTAINER_COMPOSE_DIR')
    local_repo = config('HOMELAB_COMPOSE_REPO')

    if 'link' in args:
        link_portainer_compose_files.link(
            portainer_compose_dir,
            local_repo
        )

    # TODO: Create `config` command that lets you set variables in .env
