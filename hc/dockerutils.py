#!/usr/bin/env python3


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
                value = line.replace(f"{keyword}:", "").strip()
                return value
