# -*- encoding: utf-8 -*-
"""
The Enum in python by itself is a wonderfull class that makes life very easy if
you knows how to use it. However it does not have some features that I would
like to have in my enumerations. Since several of my applications are Data
base based. I de needed an enumeration able to convert thing to strings on
the fly so I did not have to care about implicit convertion and that stuff.
Therefore I made two classes that are meant to serve as constant definitions to
group some values and ake the tast of usingthem in queries quite easy.

* ExtendedEnum: Basic Class intended to Add the automatic covnertion to the
  constants when concatenated in a string (therefore when converted to
  queries).
* LabeledEnum: Similar to ExtendedEnum. It provides the option to give a tag
  (string) to each constant in order to generate user friendly associations.
  For instance, if you want to enumerate some values to display in a
  dropdown, the value would be the associated ID of the constant, and it
  will hve a defined label associated to it that you could should to the
  user as a string.

There might come some other neumeration types, but for the moment being is
not expected.


.. Attention::
    For some reason it is was not possible for me to get the docstring in this
    page automatically. Use the link to the source code in order to see the
    docstrings.

    The docstrings include the tests to.

"""

from enum import Enum


class ExtendedEnum(Enum):
    """
    Extends the normal Enum for single constants in order to implement
    string conversion of the values and listing as dictionaries.

    >>> class MyExtendedEnumeration(ExtendedEnum):
    ...     FOO1 = 'BAR 1'
    ...     FOO2 = 'BAR 2'

    >>> MyExtendedEnumeration.FOO1 == MyExtendedEnumeration.FOO1
    True
    >>> MyExtendedEnumeration.FOO1 is MyExtendedEnumeration.FOO1
    True
    >>> MyExtendedEnumeration.FOO1 == MyExtendedEnumeration.FOO2
    False
    >>> MyExtendedEnumeration.FOO1 is MyExtendedEnumeration.FOO2
    False
    >>> MyExtendedEnumeration.FOO1 is not MyExtendedEnumeration.FOO2
    True
    >>> str(MyExtendedEnumeration.FOO1)
    'BAR 1'


    """

    def __str__(self):
        """
        String form of an enumeration composed by the name of the
        variable and its value in an equality.

        :return: str

        >>> class MyEnum(ExtendedEnum):
        ...     FOO1 = 'BAR 1'
        ...     FOO2 = 3.14
        >>> str(MyEnum.FOO1)
        'BAR 1'
        >>> str(MyEnum.FOO2)
        '3.14'

        """
        return str(self.value)

    @classmethod
    def as_dict(cls, inverted=False):
        """
        Returns a dictionary where they ids are the variable name and
        the values the value of the id.

        :return: tuple of as_tuples

        >>> class MyLabeledEnum(ExtendedEnum):
        ...     FOO1 = 'BAR 1'
        ...     FOO2 = 'BAR 2'
        >>> MyLabeledEnum.as_dict() == {'FOO1': 'BAR 1', 'FOO2': 'BAR 2'}
        True

        >>> MyLabeledEnum.as_dict(inverted=True) == {'BAR 2': 'FOO2', 'BAR 1': 'FOO1'}
        True
        """
        if inverted:
            return {item.value: item._name_ for item in cls}
        return {item._name_: item.value for item in cls}

    @classmethod
    def as_tuples(cls):
        """
        Returns a tuple formed by all the values defined inside the class

        :return: tuple of strings

        >>> class MyEnum(ExtendedEnum):
        ...     FOO1 = 'BAR 1'
        ...     FOO2 = 'BAR 2'
        >>> MyEnum.as_tuples()
        (('FOO1', 'BAR 1'), ('FOO2', 'BAR 2'))
        """

        return tuple((x.name, x.value) for x in cls)

    @classmethod
    def names(cls, tuples=False):
        """
        Returns a tuple formed by all the values defined inside the class.

        :param tuples: bool: if True return a tuple, otherwise an iterator
        :return: tuple or generator

        >>> class MyEnum(ExtendedEnum):
        ...     FOO1 = 'BAR 1'
        ...     FOO2 = 'BAR 2'
        >>> MyEnum.names(tuples=True)
        ('FOO1', 'FOO2')

        >>> tuple(MyEnum.names())
        ('FOO1', 'FOO2')

        """
        names = (x.name for x in cls)
        if tuples:
            return tuple(names)
        return names

    @classmethod
    def values(cls, tuples=False):
        """
         Returns a tuple formed by all the values defined inside the class.

        :param tuples: bool: if True return a tuple, otherwise an iterator
        :return: tuple or generator

        >>> class MyEnum(ExtendedEnum):
        ...     FOO1 = 'BAR 1'
        ...     FOO2 = 'BAR 2'
        >>> MyEnum.values(tuples=True)
        ('BAR 1', 'BAR 2')

        >>> tuple(MyEnum.values())
        ('BAR 1', 'BAR 2')

        """
        if tuples:
            return tuple(x.value for x in cls)

        return (x.value for x in cls)


class LabeledEnum(Enum):
    """
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
    >>> MyLabeledEnum.FOO1 == MyLabeledEnum.FOO1
    True
    >>> MyLabeledEnum.FOO1 is not MyLabeledEnum.FOO1
    False
    >>> MyLabeledEnum.FOO1 != MyLabeledEnum.FOO2
    True
    >>> MyLabeledEnum.FOO1.id
    1
    >>> MyLabeledEnum.FOO1.label
    'BAR 1'

    """

    def __init__(self, _id, label):
        """
        This init method is called when an attribute for the class is
        defined; therefore, the main class does not require to define id_
        and label manually. This is because each Attribute defined in the
        class calls this init with the  parameters defined in the tuple.
        """

        self.id = _id
        self.label = label

    def __str__(self):
        """
        String representation of the enumeration is limited to the id

        :return: str

        >>> class MyEnum(LabeledEnum):
        ...     FOO = (1, 'BAR')
        >>> str(MyEnum.FOO)
        '1'

        """
        return str(self.id)

    def pair(self, serializer=None):
        """
        Returns a tuple consisting of (id, label) for the given value

        :param serializer: class: class used to convert the element to,
            defult is tuple
        :return: passed serializer class or tuple

        >>> class MyEnum(LabeledEnum):
        ...     FOO = (1, 'BAR')
        >>> MyEnum.FOO.pair()
        (1, 'BAR')
        >>> MyEnum.FOO.pair(list)
        [1, 'BAR']
        >>> MyEnum.FOO.pair(set) == {1, 'BAR'}
        True
        """

        pair = self.id, self.label
        if not serializer:
            return pair
        return serializer(pair)

    # Attributes

    @classmethod
    def names(cls, prefix='', suffix=''):
        """
        Returns a tuple containing all the names of the given elements with
        the given prefix and suffix concatenated at the beginning and end,
        respectively.

        :param prefix: str: string to add at the beginning of the names
        :param suffix: str: string to add at the end of the names
        :return: generator

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')

        >>> tuple(MyEnum.names())
        ('FOO1', 'FOO2')

        >>> type(MyEnum.names())
        <class 'generator'>
        >>> tuple(MyEnum.names(suffix='_s'))
        ('FOO1_s', 'FOO2_s')
        >>> for name in MyEnum.names('p_', '_s'):
        ...    name
        'p_FOO1_s'
        'p_FOO2_s'

        """

        if not prefix and not suffix:
            return (x.name for x in cls)
        return ('{}{}{}'.format(prefix, x.name, suffix) for x in cls)

    @classmethod
    def ids(cls, tuples=False):
        """
        Returns a generator or tuple containing just the ids of all the created
        constants inside the class as elements.

        :param: tuples: bool: If true returns a tuple, otherwise a generator
        :return: generator

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> tuple(MyEnum.ids())
        (1, 2, 3)
        >>> 2 in MyEnum.ids()
        True
        >>> 4 in MyEnum.ids()
        False
        >>> MyEnum.ids(tuples=True)
        (1, 2, 3)

        """
        ids = (x.id for x in cls)
        if tuples:
            return tuple(ids)
        return ids

    @classmethod
    def tuples(cls, tuples=False):
        """
        Returns a generator or tuple containing just the ids of all the created
        constants inside the class as elements.

        :param: tuples: bool: If true returns a tuple, otherwise a generator
        :return: generator

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> tuple(MyEnum.tuples())
        ((1, 'BAR 1'), (2, 'BAR 2'), (3, 'BAR 3'))

        >>> (1, 'BAR 1') in MyEnum.tuples()
        True

        >>> 2 in MyEnum.tuples()
        False

        >>> MyEnum.tuples(tuples=True)
        ((1, 'BAR 1'), (2, 'BAR 2'), (3, 'BAR 3'))

        """
        ids = (x.value for x in cls)
        if tuples:
            return tuple(ids)
        return ids

    @classmethod
    def dictionaries(cls, inverted=False):
        """
        Returns a generator or tuple containing just the ids of all the created
        constants inside the class as elements.

        :param: tuples: bool: If true returns a tuple, otherwise a generator
        :return: generator

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> MyEnum.dictionaries()
        {1: 'BAR 1', 2: 'BAR 2', 3: 'BAR 3'}
        >>> MyEnum.dictionaries(True)
        {'BAR 1': 1, 'BAR 2': 2, 'BAR 3': 3}

        """

        if inverted:
            return {x.label: x.id for x in cls}
        return {x.id: x.label for x in cls}

    @classmethod
    def labels(cls, tuples=False):
        """ Returns a generator or tuple containing just the labels of all the
        created constants inside the class as elements.

        :return: generator

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> tuple(MyEnum.labels())
        ('BAR 1', 'BAR 2', 'BAR 3')
        >>> 'BAR 3' in tuple(MyEnum.labels())
        True
        >>> 'BAR 4' in tuple(MyEnum.labels())
        False
        >>> MyEnum.labels(True)
        ('BAR 1', 'BAR 2', 'BAR 3')
        """
        labels = (x.label for x in cls)
        if tuples:
            return tuple(labels)
        return labels

    @classmethod
    def triads(cls, tuples=False):
        """
        Returns a generator containing tuples with the name, id and label of
        each constant of the class

        :return: generator: generator containing tuples consisting

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')

        >>> tuple(MyEnum.triads())
        (('FOO1', 1, 'BAR 1'), ('FOO2', 2, 'BAR 2'))

        >>> type(MyEnum.triads())
        <class 'generator'>
        >>> for name, id, label in MyEnum.triads():
        ...    (name, id, label)
        ('FOO1', 1, 'BAR 1')
        ('FOO2', 2, 'BAR 2')


        >>> MyEnum.triads(True)
        (('FOO1', 1, 'BAR 1'), ('FOO2', 2, 'BAR 2'))

        """
        triads = ((x.name, x.id, x.label) for x in cls)
        if tuples:
            return tuple(triads)
        return triads

    # Search

    @classmethod
    def with_key(cls, id_, as_tuples=False):
        """
        Returns a generatos/tuple containing ALL the elements with the given id
        (or an empty tuple if nothing found)

        :param as_tuples: bool: if True returns a tuple, otherwise a generator
        :param id_: different values: id to filter with
        :return: tuple

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        ...     FOO4 = (3, 'BAR 4')

        >>> type(MyEnum.with_key(1))
        <class 'generator'>

        >>> MyEnum.FOO3 in MyEnum.with_key(3, True)
        True
        >>> MyEnum.FOO4 in MyEnum.with_key(3, True)
        True

        >>> MyEnum.FOO1 in MyEnum.with_key(-1)
        False
        >>> len([e for e in MyEnum.with_key(-1)])
        0

        """
        elements = (e for e in cls if e.id == id_)
        if as_tuples:
            return tuple(elements)
        return elements

    @classmethod
    def from_key(cls, id_):
        """
        Returns THE FIRST element found that has the given id or None if
        nothing is found

        :param id_: different values: id to search for
        :return: different types/None

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        ...     FOO4 = (3, 'BAR 4')

        >>> MyEnum.from_key(1)
        <MyEnum.FOO1: (1, 'BAR 1')>
        >>> MyEnum.from_key(-1) == None
        True
        >>> MyEnum.from_key(-1) is None
        True

        """

        return next(iter(filter(lambda x: x.id == id_, cls)), None)

    @classmethod
    def with_label(cls, label, as_tuples=False):
        """
        Searches for elements and returns always the first one found from
        within the given parameters

        :param label: different values: label to search for
        :param as_tuples: bool: If True return a tuple, otherwise a generator
        :return: str: label associated to the given label


        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 1')
        ...     FOO3 = (3, 'BAR 3')

        >>> tuple(MyEnum.with_label('BAR 1'))
        (<MyEnum.FOO1: (1, 'BAR 1')>, <MyEnum.FOO2: (2, 'BAR 1')>)

        >>> len([e for e in MyEnum.with_label('BAR 1')])
        2

        >>> MyEnum.FOO2 in MyEnum.with_label('BAR 2') == ()
        False
        >>> MyEnum.with_label('BAR 3', True)
        (<MyEnum.FOO3: (3, 'BAR 3')>,)

        """

        elements = (e for e in cls if e.label == label)
        if as_tuples:
            return tuple(elements)
        return elements

    @classmethod
    def from_label(cls, label):
        """
        Returns THE FIRST element found that has the given label or None if
        nothing is found

        :param label: different values: label to search for
        :return: different values or None

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')

        >>> MyEnum.from_label('BAR 1')
        <MyEnum.FOO1: (1, 'BAR 1')>
        >>> MyEnum.from_label('BAR 3')
        <MyEnum.FOO3: (3, 'BAR 3')>
        >>> MyEnum.from_label('BAR 4') == None
        True
        >>> MyEnum.from_label('BAR 4') is None
        True

        """
        return next(iter(filter(lambda x: x.label == label, cls)), None)

    # Serialization
    @classmethod
    def as_tuples(cls):
        """
        Returns a tuple formed by pairs (id, label) for all the elements
        inside the class

        :return: tuple of tuples

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')

        >>> MyEnum.as_tuples()
        (('FOO1', (1, 'BAR 1')), ('FOO2', (2, 'BAR 2')), ('FOO3', (3, 'BAR 3')))

        >>> ('FOO1', (1, 'BAR 1')) in MyEnum.as_tuples()
        True
        """
        return tuple((e.name, e.pair()) for e in cls)

    @classmethod
    def as_dict(cls):
        """ Returns a dictionary where they ids are the variable name and
        the values the value of the id.

        :return: tuple of as_tuples

        >>> class MyLabeledEnum(ExtendedEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        >>> MyLabeledEnum.as_dict() == {'FOO1': (1, 'BAR 1'), 'FOO2': (2, 'BAR 2')}
        True

        >>> MyLabeledEnum.as_dict() == {'BAR 2': 'FOO2', 'BAR 1': 'FOO1'}
        False
        """
        return {e.name: e.pair() for e in cls}

    @classmethod
    def describe(cls):
        """
        Prints in the console a table a horrible table showing the id and
        their corresponding values of all the definitions inside the class

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> MyEnum.describe()
        Class: MyEnum
            Ids | Label
            --------------
              1 | BAR 1
              2 | BAR 2
              3 | BAR 3
        """

        keys = list(map(str, cls.ids())) + ["Ids"]

        max_ = max(tuple(map(len, keys)))
        if max_ < 2:
            max_ = 2
        row_format = "    {:>" + str(max_) + "}" + " | {:}"
        headers = ["Ids", "Label"]
        print("Class: {}".format(cls.__name__))
        headerline = row_format.format(*headers)
        print(headerline)
        print("    " + "-" * (len(headerline) - 1))

        for item in cls:
            print(row_format.format(str(item.id), item.label))

    @classmethod
    def label2id(cls, label):
        """Return the first coincidence complete element that has the given id

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> MyEnum.label2id('BAR 1')
        1
        >>> MyEnum.label2id('BAR 3')
        3
        >>> MyEnum.label2id('BAR 12') == None
        True
        """
        element = cls.from_label(label)
        return element.id if element else None

    @classmethod
    def label2ids(cls, label, as_tuples=False):
        """Return the first coincidence complete element that has the given id

        :param label: different values, label to search for
        :param as_tuples: bool: if True returns a tuple, otherwise a generator

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> tuple(MyEnum.label2ids('BAR 1'))
        (1,)
        >>> MyEnum.label2ids('BAR 3', True)
        (3,)
        >>> len([e for e in MyEnum.label2ids('BAR 12')])
        0
        """
        ids = (e.id for e in cls if e.label == label)
        if as_tuples:
            return tuple(ids)
        return ids

    @classmethod
    def id2label(cls, key):
        """Return the first coincidence complete element that has the given id

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> MyEnum.id2label(1)
        'BAR 1'
        >>> MyEnum.id2label(4) == None
        True
        """

        element = cls.from_key(key)
        return element.label if element else None

    @classmethod
    def id2labels(cls, id_, as_tuples=False):
        """Return the first coincidence complete element that has the given id

        :param id_: different values, id to search for
        :param as_tuples: bool: if True returns a tuple, otherwise a generator

        >>> class MyEnum(LabeledEnum):
        ...     FOO1 = (1, 'BAR 1')
        ...     FOO2 = (2, 'BAR 2')
        ...     FOO3 = (3, 'BAR 3')
        >>> tuple(MyEnum.id2labels(1))
        ('BAR 1',)
        >>> MyEnum.id2labels(1, True)
        ('BAR 1',)
        >>> len([e for e in MyEnum.id2labels(4)])
        0
        """

        labels = (e.label for e in cls if e.id == id_)
        if as_tuples:
            return tuple(labels)
        return labels


if __name__ == "__main__":
    import doctest
    doctest.testmod()
