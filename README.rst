CGM tools
=========
A set of very simple tools and utils to work with
  * Constants
  * Files
  * Dictionaries

(Just constants is properly documented and tested).
This package is under development, therefore just the branch Dev is currently existing. I'm very sorry that at the moment the documentaiton and tests are incomplete, but that is how experiments llok like.

Installation
============
Since the app is not yet ready and exist just in this repository, there are few methods to install it. First you need to download it and use one of the following options to install. Let say you download it in a zip file with the name samanta.zip.

First option:

1. ``pip install cgm_tools.zip``

Second option:

1.  Decompress the downloaded file, you will see the same files you see in Github/Bitbucket. Here you have several options for installation. Since we are under development, I suggest the following:
2. ``python setup.py develop``

This will allow you to have the package installed in development mode.

Features
========
The features in Samanta are very simple and are the basics that will be used in all my web apps in the future:

* constants: Extension ofr ``enum.Enum``. It provides the a class to add labels to the enumeration in case of needing machine friendly and user friendly information. These values are called id and label. Check the incode documentation for further details.
    * Well documented and tested


The ExtendedEnum:
```python:
    Extended enumeration class: implements a label for each item and some
    methods to work with ids and labels as with dictionaries. Each
    attribute of the class is formed by a id and a label in the format:
    FOO = (int, foo).


    :param _id: different types: value used to define the key of an
       element, recommended: int
    :param label: str: label to relate to the id


    >>> class MyLabeledEnum(LabeledEnum):
    ...     FOO1 = (1, 'BAR 1')
    ...     FOO2 = (2, 'BAR 2')
    ...     FOO3 = (3, 'BAR 3')


    >>> MyLabeledEnum.FOO1.id
    1
    >>> MyLabeledEnum.FOO1.label
    'BAR 1'

    >>> MyLabeledEnum.FOO1 is MyLabeledEnum.FOO1
    True
    >>> MyLabeledEnum.names(tuples=True)
    ('FOO1', 'FOO2', 'FOO3')
    >>> MyLabeledEnum.ids(tuples=True)
    (1, 2, 3)
    >>> MyLabeledEnum.tuples(tuples=True)
    ((1, 'BAR 1'), (2, 'BAR 2'), (3, 'BAR 3'))
    >>> MyLabeledEnum.dictionaries()
    {1: 'BAR 1', 2: 'BAR 2', 3: 'BAR 3'}
    >>> MyLabeledEnum.dictionaries(True)
    {'BAR 1': 1, 'BAR 2': 2, 'BAR 3': 3}
    >>> MyLabeledEnum.from_key(1)
    <MyEnum.FOO1: (1, 'BAR 1')>
    >>> MyLabeledEnum.from_key(-1) == None
    True
```

The rest of the components are not recomended to be used as they are, since they are being modified in the experimental-secret repository almost every day.

* Dictionaries: Abstractions to be used as configuration storages, that validates changes from and passed parameters while using a basic structure.

* Files: Wrappers for the os package to make life easier, they provide new methods for checks, directly writting and reading text files.

* Structures: combination of 'Dictionaries' and 'Files' in order to generate configuration files.



Further options
===============
Just for Linux.

If you look at the source of the file, you will notice that there is a makefile inside. You can use it in order to perform some operations
to use it you need to be in the same file than the makefile. The commands are very simple.

``make <option>``

With the optionc:

* ``clean-pyc``: Removes all python compiled files (pyc) 
* ``test``: Run unit tests and doctests for the complete package.
* ``document``: Runs sphinx to generate the documentation. It can be found afterwards in the folder 'docs\build\html'
* ``install``: Installs the package using pip
* ``install-devel``: Install the package using python in development mode

