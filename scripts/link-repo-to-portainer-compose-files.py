#!/usr/bin/sudo /usr/bin/python3

from os import listdir, path
from decouple import config
from subprocess import run
from utils import bytes_to_ascii, bytes_to_ascii_list, create_dir_if_not_extant


stacks =  {
    'network-stack': ['duckdns', 'pihole-unbound'],
    'grafana-stack': ['telegraf', 'influxdb', 'chronograf',  'grafana'],
    'heimdall-stack': ['heimdall'],
    'home-stack': ['grocy'],
    'rss-stack': ['freshrss', 'mariadb']
}


def get_app_name_from_compose_file(compose_file):
    keyword = 'container_name:'
    with open(compose_file) as file:
        for line in file:
            if keyword in line:
                app_name = line.replace(keyword, '').strip()
    return app_name


def get_stack_name_from_app_name(app):
    for stack in stacks:
        if app in stacks[stack]:
            return stack


def print_output(output):
    for stdout, stderr in output:
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)


def link_compose_files(compose_file):
    output = []

    if not path.exists(linked_compose_file):
        process = run([
            'sudo',
            'ln',
            compose_file,
            linked_compose_file
        ],
        capture_output=True)

        process_output = bytes_to_ascii_list(stdout, stderr)
        output.append(process_output)
        
    return output


rootdir = config('PORTAINER_COMPOSE_DIR')
local_repo = config('HOMELAB_COMPOSE_REPO')

# for subdir in listdir(rootdir):
#     compose_file = f'{rootdir}/{subdir}/docker-compose.yml'
#     app_name = get_app_name_from_compose_file(compose_file)
#     stack_name = get_stack_name_from_app_name(app_name)
#     stack_dir = f'{local_repo}/{stack_name}'
#     create_dir_if_not_extant(stack_dir)
#     linked_compose_file = f'{stack_dir}/docker-compose.yml'
#     output = link_compose_files(linked_compose_file)
#     print_output(output)

print(rootdir, local_repo)