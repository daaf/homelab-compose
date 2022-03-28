from os import path, mkdir
from subprocess import run


def bytes_to_ascii(b):
    """Decode bytes to ASCII and remove whitespace."""
    return b.decode('ascii').strip()


def bytes_to_ascii_list(*args):
    """Return a list of strings decoded from a sequence of bytes."""
    return [bytes_to_ascii(b) for b in args]


def create_dir_if_not_extant(path):
    """Create a directory at the specified path if it doesn't already exist."""
    if not path.exists(path):
        mkdir(path)


def ln(existing_path, link_path):
    """Use the ln command to create a hard link to a file."""
    output = []

    if not path.exists(link_path):
        process = run([
            'sudo',
            'ln',
            existing_path,
            link_path
        ], capture_output=True)
        process_output = bytes_to_ascii_list(process.stdout, process.stderr)
        output.append(process_output)

    return output


def print_process_output(output):
    """Print the output of a Python subprocess."""
    for stdout, stderr in output:
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)


def get_compose_attribute_value(compose_file, keyword):
    """
    Get the value of an attribute from a Docker Compose file.

    :param compose_file: The Docker Compose file to search.
    :param keyword: The keyword of the value to retrieve.
    :returns: If the keyword is found, the value corresponding to the keyword.
    """
    with open(compose_file) as file:
        for line in file:
            if keyword in line:
                value = line.replace(f'{keyword}:', '').strip()
                return value
