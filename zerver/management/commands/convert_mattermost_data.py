import argparse
import os
from typing import Any

'''
Example usage for testing purposes:

    ./manage.py convert_mattermost_data mmbulk_data_mar8_2019.json --output mm_export
    ./manage.py import --destroy-rebuild-database mattermost mm_export

Test out the realm:
    ./tools/run-dev.py
    go to browser and use your dev url

spec:
https://docs.mattermost.com/administration/bulk-export.html
'''

from django.core.management.base import BaseCommand, CommandParser

from zerver.data_import.mattermost import do_convert_data

class Command(BaseCommand):
    help = """Convert the mattermost data into Zulip data format."""

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('mattermost_data_dir',
                            metavar='<mattermost data directory>',
                            help="Directory containing the exported json file and exported_emoji(Optional) directory.")

        parser.add_argument('--output', dest='output_dir',
                            action="store",
                            help='Directory to write exported data to.')

        parser.add_argument('--mask', dest='masking_content',
                            action="store_true",
                            help='Mask the content for privacy during QA.')

        parser.formatter_class = argparse.RawTextHelpFormatter

    def handle(self, *args: Any, **options: Any) -> None:
        output_dir = options["output_dir"]

        if output_dir is None:
            print("You need to specify --output <output directory>")
            exit(1)

        if os.path.exists(output_dir) and not os.path.isdir(output_dir):
            print(output_dir + " is not a directory")
            exit(1)

        os.makedirs(output_dir, exist_ok=True)

        if os.listdir(output_dir):
            print('Output directory should be empty!')
            exit(1)

        output_dir = os.path.realpath(output_dir)

        data_dir = options['mattermost_data_dir']
        if not os.path.exists(data_dir):
            print("Directory not found: '%s'" % (data_dir,))
            exit(1)

        print("Converting Data ...")
        do_convert_data(
            mattermost_data_dir=data_dir,
            output_dir=output_dir,
            masking_content=options.get('masking_content', False),
        )
