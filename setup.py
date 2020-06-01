#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Jinja2==2.10.3', 'Click==7.0']

test_requirements = [
    'pip==19.2.3',
    'bump2version==0.5.11',
    'wheel==0.33.6',
    'watchdog==0.9.0',
    'flake8==3.7.8',
    'tox==3.14.0',
    'coverage==4.5.4',
    'Sphinx==1.8.5',
    'twine==1.14.0',
    'Click==7.0',
    'pytest==4.6.5',
    'pytest-runner==5.1',
    'Jinja2==2.10.3'
]

setup(
    author="Scott Rothbarth",
    author_email='srserves85@gmail.com',
    python_requires='>3.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="avro-to-python is a light tool for compiling avro schema files (.avsc) to python classes making using avro schemata easy.",
    entry_points={
        'console_scripts': [
            'avro-to-python=avro_to_python.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='avro-to-python',
    name='avro_to_python',
    packages=find_packages(include=['avro_to_python', 'avro_to_python.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/srserves85/avro-to-python',
    version='0.2.3',
    zip_safe=False,
)
