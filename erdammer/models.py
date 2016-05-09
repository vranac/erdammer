# -*- coding: utf-8 -*-

from dot import format_table_header, generate_table, format_table_row, cardinalities, format_cardinality, generate_cardinalities

column_padding = 4

def get_column_widths(columns):
    name_width = column_padding
    type_width = column_padding

    for column in columns:
        if len(column.name) > name_width:
            name_width = len(column.name)
        if len(column.type) > type_width:
            type_width = len(column.type)

    # take into account the possibility of setting the mark for primary key
    return name_width+3, type_width


def generate_padding(indent=0, filler=" "):
    return "{0:{1}<{2}}".format("", filler, indent)

def generate_table_separator(name_width=column_padding, type_width=column_padding):
    return generate_padding(name_width, "=") + generate_padding(column_padding) + generate_padding(type_width, "=")

def generate_label(name, width=None):
    name_width = len(name)
    padding = ""

    if width is not None:
        difference = width - name_width
        if difference < 0:
            raise ValueError()

        padding = generate_padding(difference)

    return name + padding

def generate_table_header(name_label,
                          type_label,
                          separator_string,
                          name_width=None,
                          type_width=None,
                          table_name_in_header=False,
                          table_name_label=""):
    name_column_label = generate_label(name_label, name_width)
    type_column_label = generate_label(type_label, type_width)

    header = separator_string + '\n'

    if table_name_in_header:
        header_separator_string = generate_padding(name_width + column_padding + type_width, "-")

        header += table_name_label + '\n' + header_separator_string + '\n'


    header += name_column_label + generate_padding(column_padding) + type_column_label + '\n'
    header += separator_string + '\n'

    return header

class Exportable():
    """Abstract class to represent all the objects that are exportable"""

    def to_csv(self):
        """Transforms the object into csv file output"""
        raise NotImplementedError()

    def to_rst(self):
        """Tranforms the object into ReStructured text"""
        raise NotImplementedError()

    def to_dot(self):
        """Transforms the object into dot format"""
        raise NotImplementedError()

class Table(Exportable):
    """ Represents a Table object that can be exported"""
    def __init__(self, name, columns):
        """
        :param name: (unicode) Name of the table
        :param columns: (list) List of the table columns
        :return:
        """

        self.name = name
        self.columns = columns

    def to_rst(self, table_names_in_header=False):
        """
        Returns a rst table representation

        :returns:
        =========    ============
        Name         Type
        =========    ============
        something    varchar(255)
        =========    ============
        """

        name_width, type_width = get_column_widths(self.columns)

        separator_string = generate_table_separator(name_width, type_width)

        header = generate_table_header("Name", "Type", separator_string, name_width, type_width, table_names_in_header, self.name)

        return header + ''.join(column.to_rst(name_width, type_width) for column in self.columns) + separator_string + '\n'

    def to_csv(self):
        header = "Name,Type\n"
        return header + ''.join(column.to_csv() for column in self.columns)

    def to_dot(self):
        body = ''.join(column.to_dot() for column in self.columns)
        header = format_table_header(self.name)

        return generate_table(self.name, header, body)

class Column(Exportable):
    """ Represents a Column object that can be exported"""

    def __init__(self, name, type=None, is_primary_key=False):
        """
        :param name: (unicode) Name of the column
        :param type: (unicode) Type of the column
        :param is_primary_key: (bool) Is the column primary key
        :return:
        """

        self.name = name
        self.type = type
        self.is_primary_key = is_primary_key

    def primary_key_symbol(self, use_rst = False):
        return ('\* ' if use_rst else '* ') if self.is_primary_key else ''

    def to_rst(self, name_width=4, type_width=4):
        name_column_label = generate_label(self.primary_key_symbol(True) + self.name, name_width)
        type_column_label = generate_label(self.type, type_width)

        return name_column_label + generate_padding(4) + type_column_label + '\n'

    def to_csv(self):
        return "{0}{1},{2}\n".format(self.primary_key_symbol(),self.name, self.type)

    def to_dot(self):
        return format_table_row(self.name, self.type, self.is_primary_key)

class Relationship(Exportable):
    """ Represents a Foreign Key object that can be exported"""


    def __init__(self, right_column, left_column, right_cardinality=None, left_cardinality=None):
        if right_cardinality not in cardinalities.keys()\
           or left_cardinality not in cardinalities.keys():
            raise ValueError('Cardinality should be in {}"'.format(cardinalities.keys()))

        self.right_column = right_column
        self.left_column = left_column
        self.right_cardinality = right_cardinality
        self.left_cardinality = left_cardinality


    def to_dot(self):
        if self.right_cardinality == self.left_cardinality == '':
            return ''

        cardinalities = []

        # if self.left_cardinality != '':
        #     cardinalities.append('tail' +
        #                  format_cardinality(self.left_cardinality))
        #
        # if self.right_cardinality != '':
        #     cardinalities.append('head' +
        #                          format_cardinality(self.right_cardinality))

        return generate_cardinalities(self.left_column, self.right_column, cardinalities)
