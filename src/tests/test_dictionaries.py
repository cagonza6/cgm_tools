from cgm_tools.dictionaries import ConfigDict
import unittest


class TestStringMethods(unittest.TestCase):
    """
    Class intended to test the dictionaries module
    """

    def test_correct_init(self):
        """
        Makes sure that the initialization takes parameters that are all
        covered by the defaults parameters. possibilities are there como
        less parameters, but not more or any different.

        :return: None
        """
        defaults = {'a': 0, 'b': 0, 'c': 0}
        data_less = {'a': 1, 'b': 2}
        data_ok = {'a': 1, 'b': 2, 'c': 3}
        data_short = {'a': 1, 'b': 2, 'd': 3}
        data_long = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

        # initialises a ConfigDict with correct parameter to construct
        # same values in data and defaults
        ok = ConfigDict(data_ok, defaults)
        # if no errors, given data should be the same than config data
        self.assertDictEqual(ok.data, data_ok)

        # A id not covered by default should complain
        with self.assertRaises(NameError):
            ConfigDict(data_short, defaults)

        # data with less parameters,
        less = ConfigDict(data_less, defaults)
        # updated data
        updated_less = defaults.copy()
        updated_less.update({'c': 3})
        self.assertDictEqual(ok.data, data_ok)

        # data with more parameters
        with self.assertRaises(NameError):
            ConfigDict(data_long, defaults)

    def test_defaults_use(self):
        """Make sure that the file retrieves the default value for each
        parameter not passed in the parameter data.

        :return: None
        """
        defaults = {'a': 0, 'b': 0, 'c': 0}
        data_ok = {'a': 1, 'b': 2, 'c': 3}
        data_less = {}  # empty!

        # Correct initialization
        full = ConfigDict(data_ok, defaults)

        # config data should be at least equivalent to the given one
        self.assertDictEqual(full.data, data_ok)

        # data with less parameters,
        less = ConfigDict(data_less, defaults)
        # its a non given value should be same than the default
        for k, v in defaults.items():
            self.assertEqual(getattr(less, k), v)

    def test_data_read(self):
        """
        Makes sure that parameters correspond to what is it passed to the
        constructor

        :return: None
        """
        defaults = {'a': 0, 'b': 0, 'c': 0}
        data_ok = {'a': 1, 'b': 2, 'c': 3}

        config = ConfigDict(data_ok, defaults)

        for k, v in data_ok.items():
            self.assertEqual(getattr(config, k), v)

    def test_data_edit(self):
        """

        :return: None
        """

        defaults = {'a': 0, 'b': 0, 'c': 0}
        data_ok = {'a': 1, 'b': 2, 'c': 3}
        data_mod = {k: -v for k, v in data_ok.items()}

        config = ConfigDict(data_ok, defaults)

        # udpate the values one by one
        for k, v in data_mod.items():
            setattr(config, k, v)

        # check if changes tuk place
        for k, v in defaults.items():
            self.assertNotEqual(getattr(config, k), defaults[k])
            self.assertNotEqual(getattr(config, k), data_ok[k])
            # differences
            self.assertEqual(getattr(config, k), data_mod[k])
        # and same thing with the internal dict
        self.assertDictEqual(config.data, data_mod)

    def test_data_update(self):
        """
        make sure that the update function actually updates the values
        :return: None
        """

        defaults = {'a': 0, 'b': 0, 'c': 0}
        data_ok = {'a': 1, 'b': 2, 'c': 3}
        data_mod = {k: -v for k, v in data_ok.items()}
        data_mod_long = data_mod.copy()
        data_mod_long['z'] = 3.14

        config = ConfigDict(data_ok, defaults)
        config.update(data_mod)

        # and same thing with the internal dict
        self.assertDictEqual(config.data, data_mod)
        # update should fail if non existing values are passed
        with self.assertRaises(AttributeError):
            config.update(data_mod_long, silent=False)

        # not fail if silent, it should have the previous data in
        config.update(data_mod_long, silent=True)
        self.assertDictEqual(config.data, data_mod)

    def test_data_creation(self):
        """
        Checks that the addition of values not provided during
        initialization can not be added by attributes

        :return: None
        """

        defaults = {'a': 0, 'b': 0, 'c': 0}
        data_ok = {'a': 1, 'b': 2, 'c': 3}
        config = ConfigDict(data_ok, defaults)

        # try to create a new parameter
        with self.assertRaises(AttributeError):
            config.d = -1

    def test_diff(self):
        """
        Checks that the addition of values not provided during
        initialization can not be added by attributes

        :return: None
        """

        defaults = {'a': 0, 'b': 0, 'c': 0, 'z': 9}
        data_ok = {'a': 1, 'b': 2, 'c': 3}
        config = ConfigDict(data_ok, defaults)

        # try to create a new parameter
        config.a = -1
        config.z = -9
        self.assertDictEqual(config.diff, {'a': (1, -1), 'z': (9, -9)})


if __name__ == '__main__':
    unittest.main()
