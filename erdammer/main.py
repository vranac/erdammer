# -*- coding: utf-8 -*-

from transformers import database_to_exportable
from dot import GRAPH_BEGINNING
from pygraphviz.agraph import AGraph
import os

def exclude_tables(tables, relationships, exclude):
    """ This function excludes the tables and relationships with tables which are
    in the exclude (lst of strings that represent tables names) """
    exclude = exclude or []
    tables_filtered = [t for t in tables if t.name not in exclude]
    relationships_filtered = [r for r in relationships
                              if r.right_col not in exclude and r.left_col not in exclude]
    return tables_filtered, relationships_filtered

def process_db(uri,
               output_directory,
               output_format='rst',
               output_name='erd',
               layout_using='neato',
               table_names_in_header=False,
               schema=None,
               svg_per_table=False,
               exclude=None):

    tables, relationships = database_to_exportable(uri, schema)

    if exclude is not None:
        exclude = exclude.split(',')

        tables, relationships = exclude_tables(tables, relationships, exclude)

    export_call = switch_export_mode[output_format]

    export_call(output_directory=output_directory,
                tables=tables,
                relationships=relationships,
                table_names_in_header=table_names_in_header,
                output_format=output_format,
                output_name=output_name,
                layout_using=layout_using,
                svg_per_table=svg_per_table)

def export_to_rst(output_directory, tables, table_names_in_header, **kwargs):
    for t in tables:
        full_path = os.path.normpath(os.path.join(output_directory, "%s.rst" % t.name))

        with open(full_path, "wb") as fh:
            fh.write(t.to_rst(table_names_in_header))

def export_to_csv(output_directory, tables, **kwargs):
    for t in tables:
        full_path = os.path.normpath(os.path.join(output_directory, "%s.csv" % t.name))

        with open(full_path, "wb") as fh:
            fh.write(t.to_csv())

def export_to_svg(output_directory, tables, relationships, svg_per_table, output_name='erd', output_format='svg', layout_using='neato', **kwargs):
    if svg_per_table:
        export_table_to_svg(output_directory=output_directory, tables=tables)

    tables_dot = '\n'.join(table.to_dot() for table in tables)
    relationships_dot = '\n'.join(relationship.to_dot() for relationship in relationships)
    dot_file = '{}\n{}\n{}\n}}'.format(GRAPH_BEGINNING, tables_dot, relationships_dot)

    graph = AGraph()
    graph = graph.from_string(dot_file)
    graph.draw(path=output_directory + "/{}.{}".format(output_name, output_format), prog=layout_using, format=output_format)

def export_table_to_svg(output_directory, tables, output_format='svg', layout_using='neato'):
    for table in tables:
        table_dot = '\n' + table.to_dot()
        dot_file = '{}\n{}\n}}'.format(GRAPH_BEGINNING, table_dot)

        graph = AGraph(directed=True)
        graph = graph.from_string(dot_file)
        graph.draw(path=output_directory + "/{}.{}".format(table.name, output_format), prog=layout_using, format=output_format)

switch_export_mode = {
    'csv': export_to_csv,
    'rst': export_to_rst,
    'svg': export_to_svg,
    'dot': export_to_svg
}