#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Jinja2==2.10.3', 'Click==7.0', 'MarkupSafe==2.0.1']

test_requirements = [
    'pip==22.0.4',
    'bump2version==1.0.1',
    'wheel==0.37.1',
    'watchdog==2.1.6',
    'flake8==4.0.1',
    'tox==3.24.5',
    'coverage==6.3.2',
    'Sphinx==4.4.0',
    'twine==3.8.0',
    'Click==8.0.4',
    'pytest==7.1.1',
    'pytest-runner==6.0.0',
    'Jinja2==3.0.3',
    'MarkupSafe==2.0.1'
]

setup(
    author="Scott Rothbarth",
    author_email='srserves85@gmail.com',
    python_requires='>3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
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
    version='1.0.0',
    zip_safe=False,
)
