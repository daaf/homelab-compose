#!/usr/bin/env python3

"""Entry point for the hc script."""

# Third party imports
from elevate import elevate

# Local imports
import cli


def main():
    elevate()
    cli.init()


if __name__ == "__main__":
    main()
