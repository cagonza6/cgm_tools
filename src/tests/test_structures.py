
from cgm_tools.structures import DictFile, DEFAULT_VERSION
from cgm_tools.dictionaries import ConfigDict

import os
import json
import unittest
import tempfile
from io import StringIO
TEMP_DIR = tempfile.mkdtemp()
TEMP_FILE = 'DictFile.txt'
TEMP_PATH = os.path.join(TEMP_DIR, TEMP_FILE)


def save_temp_dict(data_dict):
    output = StringIO()
    d = json.dumps(data_dict, sort_keys=True)
    output.write(d)
    return output


def load_path_dict(path_):
    return json.loads(path_.getvalue(), encoding='utf-8')


class TestStringMethods(unittest.TestCase):
    """
    Class intended to test the dictionaries module
    """

    def setUp(self, *args, **kwargs):
        super(TestStringMethods, self).setUp(*args, **kwargs)

        self.defaults = {'a': 0, 'b': 0, 'c': 0}
        self.data_ok = {'a': 1, 'b': 2, 'c': 3}

    def test_correct_init(self):
        """
        Makes sure that the initialization takes parameters that are all
        covered by the defaults parameters. possibilities are there como
        less parameters, but not more or any different.

        :return: None
        """
        defaults = self.defaults.copy()
        data_ok = self.data_ok.copy()

        data = save_temp_dict(data_ok)
        df = DictFile(data, defaults)

        # internals must be a ConfigDict
        self.assertEqual(type(df._internals), ConfigDict)

        # must have correct defaults
        self.assertDictEqual(df._internals.defaults, defaults)
        # an the data should be whatever is in the file
        self.assertDictEqual(df.data, data_ok)

    def test_data_edit(self):
        """
        Makes sure that the initialization takes parameters that are all
        covered by the defaults parameters. possibilities are there como
        less parameters, but not more or any different.

        :return: None
        """
        defaults = self.defaults.copy()
        data_ok = self.data_ok.copy()
        data = save_temp_dict(data_ok)

        df = DictFile(data, defaults)
        # internals must be a ConfigDict
        self.assertEqual(df.a, 1)
        df.a = 2
        self.assertEqual(df.a, 2)

    def test_data_new_attribute(self):
        """
        Makes sure that the initialization takes parameters that are all
        covered by the defaults parameters. possibilities are there como
        less parameters, but not more or any different.

        :return: None
        """
        defaults = self.defaults.copy()
        data_ok = self.data_ok.copy()
        data = save_temp_dict(data_ok)

        df = DictFile(data, defaults)
        # try to assign non existing parameter
        with self.assertRaises(AttributeError):
            df.z = -1

    def test_save(self):

        defaults = self.defaults.copy()
        data_ok = self.data_ok.copy()
        # make a defaults dictionary
        data = save_temp_dict(data_ok)
        # load the saved one with the default dictionaries
        df = DictFile(data, defaults)
        self.assertDictEqual(df.data, data_ok)

        # udpate the dict_file and save the data
        df.a = -1
        df.save()
        data_ok['a'] = -1

        updated_dict = load_path_dict(df._file.path)
        # internal info hast to match the manually modified dict
        self.assertDictEqual(df.data, data_ok)
        # loaded dict has to match the updated defaults
        self.assertDictEqual(data_ok, updated_dict)

    def test_str(self):
        defaults = self.defaults.copy()
        data_ok = self.data_ok.copy()
        # make a defaults dictionary
        data = save_temp_dict(data_ok)
        df = DictFile(data, defaults)

    def test_version(self):
        defaults = self.defaults.copy()
        data_ok = self.data_ok.copy()
        defaults['_version__'] = DEFAULT_VERSION - 1
        # make a defaults dictionary
        data = save_temp_dict(data_ok)
        df = DictFile(data, defaults)

        self.assertEqual(df._version, DEFAULT_VERSION)


#
#     def test_defaults_use(self):
#         """
#
#         :return: None
#         """
#         defaults = {'a': 0, 'b': 0, 'c': 0}
#         data_ok = {'a': 1, 'b': 2, 'c': 3}
#         data_less = {'a': 1, 'b': 2}
#
#         # Correct initialization
#         full = ConfigDict(data_ok, defaults)
#
#         # config data should be at least equivalent to the given one
#         self.assertDictEqual(full.data, data_ok)
#
#         # data with less parameters,
#         less = ConfigDict(data_less, defaults)
#         # its a non given value should be same than the default
#         self.assertEqual(less.c, defaults['c'])
#
#     def test_data_edit(self):
#         """
#
#         :return: None
#         """
#
#         defaults = {'a': 0, 'b': 0, 'c': 0}
#         data_ok = {'a': 1, 'b': 2, 'c': 3}
#         data_mod = data_ok.copy()
#                 # Correct initialization
#         config = ConfigDict(data_ok, defaults)
#
#         # new value for 'a'
#         new_val = -1
#         # update the dictionary
#         config.a = new_val
#         data_mod['a'] = new_val
#
#         # it changes the data
#         self.assertEqual(config.a, new_val)  # check update
#         self.assertNotEqual(config.a, data_ok['a'])  # check differences
#         self.assertNotEqual(config.a, defaults['a'])
#
#     def test_data_creation(self):
#         """
#         Checks that the addition of values not provided during
#         initialization can not be added by attributes
#
#         :return: None
#         """
#
#         defaults = {'a': 0, 'b': 0, 'c': 0}
#         data_ok = {'a': 1, 'b': 2, 'c': 3}
#         config = ConfigDict(data_ok, defaults)
#
#         # try to create a new parameter
#         with self.assertRaises(NameError):
#             config.d = -1
#
#     def test_data_update(self):
#         """
#         Checks that the addition of values not provided during
#         initialization can not be added by attributes
#
#         :return: None
#         """
#
#         defaults = {'a': 0, 'b': 0, 'c': 0}
#         data_ok = {'a': 1, 'b': 2, 'c': 3}
#         updates = {'a': 4, 'b': 5, 'c': 6}
#         updates_long = {'a': 4, 'b': 5, 'c': 6, 'd':7}
#
#
#         config = ConfigDict(data_ok, defaults)
#         config.update(updates)
#
#         self.assertDictEqual(config.data, updates)
#
#         # include extra ids should fail
#         with self.assertRaises(NameError):
#             config.update(updates_long)
#
#
if __name__ == '__main__':
    unittest.main()
