#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


this_directory = abspath(dirname(__file__))
with open(join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='mister_market',
    version='0.1',
    license='Apache License 2.0',
    description='A slackbot.',
    long_description=long_description,
    author='Ken Caruso',
    author_email='ken@ipl31.net',
    url='https://github.com/ipl31/mr_market',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Communications :: Chat',
    ],
    project_urls={
        'Changelog':
            'https://github.com/ipl31/mr_market/blob/master/CHANGELOG.rst',
        'Issue Tracker':
            'https://github.com/ipl31/mr_market/issues',
    },
    keywords=[
        'slack', 'bot', 'stocks'
    ],
    python_requires='>=3.5',
    install_requires=[
        'slack-bolt>=1.2.0a2',
        'slackblocks>=0.2.2',
        'iexfinance>=0.4.3',
        'requests>=2.25.0',
        'quickchart.io>=0.1.3',
        'prettytable>=2.0.0',
        'fuzzywuzzy==0.18.0',
        'python-Levenshtein>=0.12.2',
        'yfinance==0.1.55',
        'tabulate==0.8.7'
    ],
    extras_require={
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': ['mister_market = mister_market.main:main'],
    },
)
