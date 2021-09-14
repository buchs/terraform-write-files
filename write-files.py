#!/usr/bin/env python3

import json
import sys

for name, value in json.load(sys.stdin).items():

    # Skip if the file already exists with the correct value.
    try:
        with open(name) as open_file:
            if open_file.read() == value:
                continue
    except FileNotFoundError:
        pass

    # Create/overwrite the file
    with open(name, 'w') as open_file:
        open_file.write(value)

sys.stdout.write('{}')
