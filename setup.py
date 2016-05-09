#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
    'SQLAlchemy == 1.0.12',
    'click == 6.6',
    'mysql-connector-python-rf == 2.0.4',
    'pygraphviz == 1.3.1',
]

test_requirements = [
    # TODO: put package test requirements here
    'bumpversion == 0.5.3',
    'wheel == 0.23.0',
    'watchdog == 0.8.3',
    'flake8 == 2.4.1',
    'tox == 2.1.1',
    'coverage == 4.0',
    'Sphinx == 1.3.1',
    'sphinx_rtd_theme == 0.1.7',
]

setup(
    name='erdammer',
    version='0.0.5',
    description="Simple tool to generate database schema documentation",
    long_description=readme + '\n\n',
    author="Srdjan Vranac",
    author_email='vranac@gmail.com',
    url='https://github.com/vranac/erdammer',
    packages=[
        'erdammer',
    ],
    package_dir={'erdammer':
                 'erdammer'},
    entry_points={
        'console_scripts': [
            'erdammer = erdammer.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='erdammer',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
