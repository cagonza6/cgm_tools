# -*- coding: UTF-8 -*-
"""
.. Warning::
    This classes must be considered highly experimental since their
    current implementation still is not something I'm happy with.
    Therefore, the implementation might change in very stong and fast.
    However, their use will remain the same.

This package contains methods to work with dictionaries. Some of them are
wrappers for other functions such a json dumps and loads, an dother are more
complicated.

* str2dic: is a wrapper for json loads, where a string is converted into a
  python dictionary.

* dic2str: is a wrapper for json loads where a dictionary is converted into a
  string.

* ConfigDict: This is a structure that maskes a dictionary that is meant for
  storing configuration. This Class will be initialized with some defaults that
  contain all the possible settings that can be stored by the class and the
  actual data that contains ghe actual values that will be addressed by the
  class. The possible variables that can be stored by the class are limited to
  the variables passed in defaults, for instance, if the default has only the
  variable 'name' stored inside, there is no other value besides 'name' that
  this class could store. If the defaults have the variables 'name' and 'version'
  just those two values could be stored in the class, the idea is not to store
  unrequired information.

  Besides limiting the amount of variables, this class makes sure that any
  variables passed in the data will have a fall back in the defaults that could
  take any possible value (no type is checked). Therefore, there will  not be any
  a configuration without its fallback. Furthermore, the setting and getting
  of values of variabels is done as setting attributes. If the the class is
  called MyConfig and stored the values {'name': 'a Name', 'version': '0.0.1'}
  those variables could be addressed as:

  >>> MyConfig = ConfigDict({'name': 'Antonia', 'version':'0.0.1'}, {'name': 'UNNAMED', 'version':0})
  >>> MyConfig.version
  '0.0.1'

Setted as

  >>> MyConfig.name = 'Maria'

  >>> MyConfig.name
  'Maria'

This will read and store the values as in the examples.

"""
import json


def str2dic(str_):
    """shortcut to convert a string into a dictionary. This is a wrapper to
    convert to json
    """
    return json.loads(str_)


def dic2str(dict_, indent=2, separators=None):
    """shortcut to convert a dictionary into string. This is a wrapper to
    json.dumps
    """
    assert issubclass(dict_, dict)
    kwargs = {'sort_keys': True, 'indent': indent}

    if separators is not None:
        kwargs['separators'] = (',', ': ')

    return json.dumps(dict_, **kwargs)


class ConfigDict(object):
    __slots__ = ['defaults', 'initials', '_attributes_']

    def __init__(self, config_data, defaults):
        """ Simple abstraction to use dictionaries as configuration
        elements where each id of the dictionary can be accessed as
        __file.
        Each ConfigDict has to be declared with configuration data
        (config_data) that will be abstracted as __file and a 'defaults'
        structure that contains default values to be used as fallback in
        case that something was not declared in config_data.

        :param config_data: dict: contains the values to address as
          configurations
        :param defaults: dict: general structure with fall back values for
          config data.

        >>> defaults = {'param1': 'P 1', 'param2': 'P 2','param3': 'D 3' }
        >>> configs = {'param3': 'P 3'}

        >>> cd = ConfigDict(configs, defaults)
        >>> cd.param1
        'P 1'
        >>> cd.param2
        'P 2'
        >>> cd.param2 = 'hola'
        >>> cd.param2
        'hola'
        >>> cd.data == {'param1': 'P 1', 'param3': 'P 3'}
        False
        >>> cd.data == {'param1': 'P 1', 'param2': 'hola', 'param3':'P 3'}
        True
        >>> cd.update({'param4':'P 4'}, silent=True)
        >>> cd.data == {'param1': 'P 1', 'param2': 'hola', 'param3':'P 3',
        ...             'param4': "P 4" }
        False
        """

        assert type(defaults) == dict
        assert type(config_data) == dict

        # make sure the given data is within the defaults:
        for k in config_data.keys():
            if k not in defaults.keys():
                raise NameError("Config data is providing data which is not"
                                "within the default values: '{}'".format(k))

        self._attributes_ = config_data.copy()
        self.initials = config_data.copy()
        self.defaults = defaults.copy()

    def __getattribute__(self, item):
        """ Overrides the original in order to take just values from
        the internal variables. If any atribute is requested using the '.'
        operator, it will be redirected to the internal dictionary that
        correspond to self._attributes_

        :param item: str: attribute to get.

        :return: different types
        """
        # in any internal used variable is called, return it
        if item in ['defaults', 'initials', '_attributes_']:
            return object.__getattribute__(self, item)

        # since default defines all the possible variables to have, check in
        # its ids and retourn whatever _attributes_ has in or fallback to
        # the default values
        if item in self.defaults.keys():
            # return it the value or default if it doe not exist
            return self._attributes_.get(item, self.defaults.get(item))

        # any other case, whatever the parent dictates
        return super(ConfigDict, self).__getattribute__(item)

    def __setattr__(self, key, value):
        """ same idea than in __getattribute__ but it is used to store the
        parameters in _attributes_

        :param key: str: parameter to store
        :param value: different types: value to store in the parameter

        :return: different types
        """
        # for internal use, store in them
        if key in ['defaults', 'initials', '_attributes_']:
            object.__setattr__(self, key, value)
            return

        # if is among the defaults, store it in attributes
        elif key in self.defaults.keys():
            self._attributes_[key] = value
            return

        if key not in self.defaults.keys():
            raise AttributeError(
                "{} does not accept assignment of attributes not "
                "defined in the constructor within default "
                "parameter. Options are: {}. Can't create '{}'."
                "".format(self.__class__.__name__,
                          set(self.defaults.keys()),
                          key
                          ))
        object.__setattr__(self, key, value)

    def __str__(self):
        """The string function will generate a string that informs
        containing the dictionary information
        """
        return "Configuration: \n {} ".format(json.dumps(self.data, indent=2))

    @property
    def data(self):
        """
        Collects the configuration data skipping the defaults and returns a
        dictionary with it

        :return: dict
        """
        return {k: self._attributes_.get(k, v) for k, v in
                self.defaults.items()}

    def update(self, dict_, silent=False):
        """
        Used to update the parameters and create new ones in the configuration.
        original defaults will not be modified since it is supposed since
        configurations should be compliant to general definitions.

        :param dict_: dict: dictionary containing all updates to perform
        :param silent: bool: If True raises exception if a parameter is not
            found,

        :return: None
        """
        for k, v in dict_.items():
            if k not in self.defaults.keys():
                if silent:
                    continue
                raise AttributeError("Attribute [{}] not found within "
                                     "configurations. Values are: [{}] "
                                     "".format(k, self.defaults.ids())
                                     )
            self._attributes_[k] = v

    @property
    def diff(self):
        """
        Calculates the difference between the old and new data and returns a
        dictionary where the keys are the variable names that where changed
        and the values are tuples whith the initial data in the first
        position and the second one in the second position. For each check
        the fallback of defaults is used.

        :return: dict
        """
        data = self.data

        diff = {}
        for k, v in self.defaults.items():
            current = data.get(k, self.defaults.get(k))
            initial = self.initials.get(k, self.defaults.get(k))
            if current != initial:
                diff[k] = (initial, current)
        return diff


if __name__ == '__main__':
    pass
