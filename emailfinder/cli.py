import json
import pathlib
import sys
import argparse
from typing import Final

from emailfinder.core import processing
from emailfinder import __version__


def main(argv=None):
    """The entry point for the script

   Args:
       argv (list): The list of parameters passed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', help="Domain to search", required=True)
    # parser.add_argument('--version', help="Show Emailfinder version", action='version', version=__version__)
    parser.add_argument('--output', help="Output-file to save result in json format. Example='data.json'", required=True)
    args = parser.parse_args()

    output: str = args.output
    target: str = args.domain
    MAIN_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent
    output_json: str = MAIN_DIR / output

    all_data = processing(target)
    if all_data == []:
        all_data = {
            "Error": "Nothing found in EmailFinder"
        }
    with open(output_json, "w") as jf:
        json.dump(all_data, jf, indent=2)


if __name__ == '__main__':
    main(sys.argv[1:])
