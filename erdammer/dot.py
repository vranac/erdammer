# -*- coding: utf-8 -*-

# "Lato","proxima-nova","Helvetica Neue",Arial,sans-serif

TABLE = '"{}" [label=<<FONT FACE="Helvetica" POINT-SIZE="10"><TABLE BORDER="0" CELLBORDER="1"' \
        ' CELLPADDING="5" CELLSPACING="0">{}{}</TABLE></FONT>>];'

START_CELL = '<TR><TD ALIGN="LEFT"><FONT>'
FONT_TAGS = '<FONT>{}</FONT>'
# Used for each row in the table.
ROW_TAGS = '<TR><TD{}>{}</TD></TR>'
GRAPH_BEGINNING = (' graph {\n'
                   '    splines=ortho;\n'
                   '    overlap=voronoi;\n'
                   '    rankdir=TD;\n'
                   '    node [\n'
                   '        shape=plaintext\n'
                   '    ];\n'
                   '    edge [color=gray50,\n'
                   '        minlen=2,\n'
                   '        style=solid,\n'
                   '    ];\n'
                   )

cardinalities = {
    'zero-to-many': '0..N',
    'zero-or-one': '{0,1}',
    'one-to-many': '1..N',
    'one': '1',
    '': None
}

def format_table_header(title):
    return ROW_TAGS.format(' BGCOLOR="#CCCCCC" ', '<B><FONT FACE="Helvetica" POINT-SIZE="12">{}</FONT></B>').format(title)

def generate_table(title, header, body):
    return TABLE.format(title, header, body)

def format_table_row(name, type=None, primary_key=False):
    base = ROW_TAGS.format(' ALIGN="LEFT"', '{key_opening}{col_name}{key_closing}{type}')
    return base.format(
        key_opening='<u>' if primary_key else '',
        key_closing='</u>' if primary_key else '',
        col_name=FONT_TAGS.format(name),
        type=FONT_TAGS.format(' [{}]').format(type) if type is not None else ''
    )

def format_cardinality(cardinality):
    if cardinality == '':
        return ''
    return 'label=<<FONT>{}</FONT>>'.format(cardinalities[cardinality])

def generate_cardinalities(left_column, right_column, cardinalities):
    return '"{}" -- "{}" [{}];'.format(left_column, right_column, ','.join(cardinalities))
    # return '"{}" -- "{}";'.format(left_column, right_column)
