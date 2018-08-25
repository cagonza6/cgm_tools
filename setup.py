#!/usr/bin/env python
import os
from setuptools import find_packages, setup

'''
This is an example for the possible setup of a library
located by default within the src/ folder.
All packages will be installed to python.site-packages
simply run:

    >>> python setup.py install

For a local installation or if you like to develop further

    >>> python setup.py develop --user


The test_suite located within the test/ folder
will be executed automatically.
'''

# Default version information
source_path = 'src'
__version__ = '0.1'


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='cgm_tools',
    version=__version__,
    package_dir={'': source_path},
    packages=find_packages(source_path),
    include_package_data=True,
    license='MIT License',  # example license
    description='A set of very simple tools and utils',
    long_description=README,
    url='https://github.com/cagonza6/cgm_tools',
    author='Cristian A. Gonzalez Mora',
    author_email='cagonza6@gmail.com',
    install_requires=[''],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        #'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
