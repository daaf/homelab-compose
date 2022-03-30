#!/usr/bin/env python3

"""Entry point for the hc script."""

import cli
from elevate import elevate


def main():
    elevate()
    cli.init()


if __name__ == "__main__":
    main()
