#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import click
import logging
from main import process_db

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from erdammer.version import version

logger = logging.getLogger(__name__)

def print_version(context, param, value):
    """
    Print the version of erdammer
    """
    if not value:
        return
    click.echo('erdammer %s (Python %s)' % (
        version,
        sys.version[:3]
    ))
    context.exit()


@click.command()
@click.option('--uri', '-i',
              default=None,
              type=str,
              help='Database URI to process.'
)
@click.option('--schema', '-s',
              default=None,
              type=str,
              help='Database schema to process.'
)
@click.option('--exclude', '-e',
              default=None,
              type=str,
              help='List tables in schema to exclude, separate by comma.'
)
@click.option('--table-names-in-header',
              type=bool,
              default=False,
              help='Add table names to the rst table output.'
)
@click.option('--svg-per-table',
              type=bool,
              default=False,
              help='Generate one SVG per table.'
)
@click.option('--output-format',
              default='rst',
              type=click.Choice(['rst','csv','svg','dot']),
              help='Output format, choices are: rst, csv, svg, dot. Default is rst'
)
@click.option('--layout-using',
              default='neato',
              type=click.Choice(['dot','neato']),
              help='Layout program, choices are: dot, neato. Default is neato.'
)
@click.option('--output-name',
              default='erd',
              type=str,
              help='Output svg/dot filename, default is erd.'
)
@click.option('--output-directory',
              default='./',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
              help='Output directory where you want the file(s) to be generated, default is current directory.'
)
@click.option('-V', '--version',
              is_flag=True,
              help='Show version information and exit.',
              callback=print_version,
              expose_value=False,
              is_eager=True,
)
@click.option('-v', '--verbose',
              is_flag=True,
              help='Print debug information',
              default=False
)
def main(uri,
         table_names_in_header,
         output_format,
         layout_using,
         output_name,
         output_directory,
         verbose,
         schema,
         svg_per_table,
         exclude):
    """ Simple tool to generate database schema documentation and export in svg, dot, rst or csv """
    if verbose:
        logging.basicConfig(
            format='%(levelname)s %(filename)s: %(message)s',
            level=logging.DEBUG
        )
    else:
        # Log info and above to console
        logging.basicConfig(
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )

    process_db(uri,
               schema=schema,
               output_directory=output_directory,
               layout_using=layout_using,
               output_format=output_format,
               output_name=output_name,
               table_names_in_header=table_names_in_header,
               svg_per_table=svg_per_table,
               exclude=exclude)

if __name__ == '__main__':
    main()
