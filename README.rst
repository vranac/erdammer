===============================
ERDammer
===============================

.. image:: https://img.shields.io/pypi/v/erdammer.svg
        :target: https://pypi.python.org/pypi/erdammer

.. image:: https://img.shields.io/pypi/l/erdammer.svg?maxAge=2592000
        :target: https://pypi.python.org/pypi/erdammer

.. image:: https://img.shields.io/pypi/pyversions/erdammer.svg?maxAge=2592000
        :target: https://readthedocs.org/projects/erdammer/?badge=latest



Simple tool to generate database schema documentation and export in svg, dot, rst or csv

ERDammer in current version does not mark the relationships properly, that will
be fixed in future versions.

Install
-------

.. code-block:: shell

    pip install erdammer

Usage
-----

Run `erdammer --help` for a list of options.

Things to note, to connect to the database you will have to supply a connection string uri.
For example

.. code-block:: mysql

    erdammer --uri "mysql+mysqlconnector://user:password@server/dbname" \
    --output-directory="db-schema/" --output-format=svg

By default svg export creates a file called `erd.svg` in the directory you specified in output, in this
case it is `./db-schema`.

If on the other hand you execute

.. code-block:: mysql

    erdammer --uri "mysql+mysqlconnector://user:password@server/dbname" --output-directory="db-schema/" \
    --output-format=rst

One ReStructured file per table will be created, with table name as filename.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
