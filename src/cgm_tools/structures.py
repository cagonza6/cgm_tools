# -*- coding: UTF-8 -*-
import json
import re
from cgm_tools.files import File
from cgm_tools.dictionaries import ConfigDict

DEFAULT_VERSION = 1
_SLOTS = ['_file', 'initials', '_internals', '_version']
version_key = '__version__'


def _check_version(configdata, defaults):

    # if there is in the config, take it and delete
    v = configdata.get(version_key, None)
    if v:
        del configdata[version_key]

    if not v:
        v = defaults.get(version_key, None)
        if v:
            del defaults[version_key]

    if not v:
        # print("Warning: configuration verison not found, automatically "
        #       "created as '{}'".format(DEFAULT_VERSION))
        v = DEFAULT_VERSION
    #print("Returning", v)
    return v


class DictFile(object):
    __slots__ = _SLOTS

    def __init__(self, path, defaults):
        self._file = File(path)
        content = json.loads(self._file.content)
        if type(content) != dict:
            raise ValueError("Content must be Dictionary and not '{}'".format(
                type(content)))
        #print("-->", defaults)
        self._version = _check_version(content, defaults)
        self.convert(content)
        self._internals = ConfigDict(content, defaults)

    def convert(self, content):
        #print("Calling convert")
        v_current = self._version
        v_target = DEFAULT_VERSION

        v_ = v_current
        for v in range(v_current, v_target + 1):
            if v <= v_current:
                continue
            v_str = '_{}_to_{}_'.format(v_, v)
            #print("Calling", v_str)
            fn = getattr(self, v_str)
            fn(content)
            content[version_key] = v_current + 1
            #print("Content:", content[version_key])
            v_ = v
            self._version = v

    def _1_to_2_(self):
        print("converting format 1->2")

    def __getattribute__(self, item):

        is_update = re.match('_(\d+)_to_(\d+)_', item)
        if is_update:
            return object.__getattribute__(self, item)
        # or take the internal dict, it might be there
        return super(DictFile, self).__getattribute__(item)

    def __getattr__(self, item):
        # any other attribute come from the configuration dict
        return getattr(self._internals, item)

    def __setattr__(self, key, value):
        if key in _SLOTS:
            object.__setattr__(self, key, value)
            return

        setattr(self._internals, key, value)

    @property
    def data(self):
        """
        This would never be executed but it is here for clarity reasons.
        This particular value will be taken from the internal dictionary.

        :return:
        """
        return self._internals.data

    def save(self):
        return self._file.update(json.dumps(self.data, indent=2))


if __name__ == '__main__':
    pass
