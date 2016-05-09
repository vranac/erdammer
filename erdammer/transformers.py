# -*- coding: utf-8 -*-

from models import Table, Column, Relationship

def database_to_exportable(database_uri, schema=None):
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine, MetaData

    # reflect the tables
    metadata = MetaData()
    engine = create_engine(database_uri)

    if schema is not None:
        metadata.schema = schema

    metadata.reflect(bind=engine, views=True)

    Base = automap_base(metadata=metadata)
    Base.prepare()


    return declarative_to_exportable(Base)

def declarative_to_exportable(base):
    """ Transform an SQLAlchemy Declarative Base to the exportable objects. """
    tables = [table_to_exportable(table) for table in base.metadata.tables.values()]
    relationships = [relationship_to_exportable(fk) for table in base.metadata.tables.values() for fk in table.foreign_keys]

    return tables, relationships

def table_to_exportable(table):
    """Transform an SQLAlchemy Table object to exportable object. """
    return Table(
        name=unicode(table.fullname).strip(),
        columns=[column_to_exportable(column) for column in table.columns._data.values()]
    )

def column_to_exportable(column):
    """Transform an SQLAlchemy Column object to exportable object. """
    return Column(
        name=unicode(column.name).strip(),
        type=unicode(column.type).strip(),
        is_primary_key=column.primary_key,
    )

def relationship_to_exportable(foreign_key):
    """Transform an SQLAlchemy Foreign Key object to exportable object. """
    return Relationship(
        right_column=unicode(foreign_key.parent.table.fullname),
        left_column=unicode(foreign_key._column_tokens[1]),
        right_cardinality = 'zero-or-one',
        left_cardinality = 'zero-to-many',
    )
