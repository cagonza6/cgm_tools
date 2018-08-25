# -*- coding: UTF-8 -*-
"""
.. Warning::
    This classes must be considered highly experimental since their
    current implementation still is not something I'm happy with.
    Therefore, the implementation might change in very stong and fast.
    However, their use will remain the same.

Try for an abstraction to access files (plain text) and their content by
wrapping around the os.path package.

"""
import os
import json
import codecs
from collections import OrderedDict

import io

default_encoding = 'utf-8'


class PathManager:
    """
    Common class for files and folders. It provides a set of usable
    methods for both. This is not more than a simple wrapper for the
    package 'path' methods
    """
    def __init__(self):
        pass

    @staticmethod
    def is_file(path_):
        """
        Check if the given path is a file or not

        :param path_: str: path to check for existence
        :return: bool: True if the given path corresponds to a file,
          False in any other case.

        >>> # current file as example
        >>> PathManager.is_file(__file__)
        True

        """

        return os.path.isfile(path_)

    @staticmethod
    def is_folder(path_):
        """
        Check if the given path is a folder or not

        :param path_: str: path to check for existence
        :return: bool: True if the given path corresponds to a folder,
          False in any other case.

        :param path_:
        :return:

         >>> PathManager.is_folder(__file__)
         False
         >>> # cheating, get the fodler and check if it is a folder
         >>> PathManager.is_folder(PathManager.in_folder(__file__))
         True

        """
        return os.path.isdir(path_)

    @staticmethod
    def join(path_):
        """
        join the given strings and forms a path compatible with the OS

        :param path_: list of strings
        :return: str

        >>> parts  = ["container","folder"]
        >>> PathManager.join(parts)
        'container/folder'
        """
        if type(path_) in (list, tuple):
            return os.path.join(*path_)
        return os.path.abspath(path_)

    @staticmethod
    def in_folder(path_):
        """Returns the directory component of a pathname that corresponds
        to the container of the given path (folder)

        :return: str

        >>> parts  = ["pre_container", "container", "folder", "file.ext"]
        >>> path_ = PathManager.join(parts)
        >>> PathManager.in_folder(path_)
        'pre_container/container/folder'
        >>> path_ = PathManager.join(parts[:3])
        >>> PathManager.in_folder(path_)
        'pre_container/container'

        """
        return os.path.dirname(path_)

    @staticmethod
    def file_name(path_):
        """
        Returns the name of the last level element of the given path. If
        the path corresponds to a folder, it returns the folder name, if
        the path corresponds to a file it returns the name with the
        extension.


        :return: str: name of the file or folder

        >>> parts  = ["container", "folder", "file.ext"]
        >>> pm =  PathManager()
        >>> path_ = pm.join(parts)
        >>> pm.file_name(path_)
        'file.ext'
        >>> path_ = pm.join(parts[:2])
        >>> pm.file_name(path_)
        'folder'
        """
        return os.path.basename(path_)

    @staticmethod
    def split_filename(filename):
        """Split the extension from a pathname.

        Extension is everything from the last dot to the end, ignoring
        leading dots.  Returns "(root, ext)"; ext may be empty.

        :param filename:
        :return: tuple: tuple containing the filename and the extension as
          elements

        >>> pm =  PathManager()
        >>> pm.split_filename("file.ext")
        ('file', '.ext')

        """
        return os.path.splitext(filename)

    @staticmethod
    def file_basename(path_):
        """
        Returns the name of the last level element of the given path. If
        the path corresponds to a folder, it returns the folder name, if
        the path corresponds to a file it returns the name without the extension.

        :return: the base name of the file/folder

        >>> parts  = ["container", "folder", "file.ext"]
        >>> path_ = PathManager.join(parts)
        >>> PathManager.file_basename(path_)
        'file'

        """

        filename = os.path.basename(path_)
        return os.path.splitext(filename)[0]

    @staticmethod
    def file_extension(path_):
        """
        Returns the extension of the last level element of the given
        path. If the path corresponds to a folder or the file does not
        have an extension, it returns an empty string.

        :return: str

        >>> parts  = ["container", "folder"]
        >>> path_ = PathManager.join(parts)
        >>> PathManager.file_extension(path_)
        ''
        >>> parts  = ["container", "folder", "file.ext"]
        >>> path_ = PathManager.join(parts)
        >>> PathManager.file_extension(path_)
        '.ext'

        >>> PathManager.file_extension("file.ex2")
        '.ex2'

        """
        filename = PathManager.file_name(path_)
        return PathManager.split_filename(filename)[1]

    @staticmethod
    def can_access(path_):
        """ Checks if the file can be read: os.access(path_, os.R_OK)

        :return: bool
        """
        return os.access(path_, os.R_OK)

    @staticmethod
    def can_edit(path_):
        """Cheks if the file can be edited; if can accessed and exists

        :return: bool: True if can edit, False if not
        """
        return os.path.exists(path_) and os.access(path_, os.R_OK)

    @staticmethod
    def exists(path_):
        """Checks if the path exists

        return: bool
        """
        return os.path.exists(path_)

    @staticmethod
    def fullpath(path_):
        """
        Normalized the given path eliminating double shalshes and that
        kind of akward stuff.

        :param path: str: string representing the path to normalize
        :return: str

        >>> parts  = ["pre_container", "container", "folder", "file.ext"]
        >>> path_ = PathManager.join(parts)
        >>> PathManager.fullpath(path_)
        'pre_container/container/folder/file.ext'

        """
        return os.path.normpath(path_)

    @staticmethod
    def basic_info(path_, prnt=False):
        """
        Return the basic information of the file/folder: name, path_,
        permissions, etc

        :return: dict: with the basic information
        """

        info = OrderedDict()
        info['fullpath '] = PathManager.fullpath(path_)
        info['in_folder'] = PathManager.in_folder(path_)
        info['file_name'] = PathManager.file_name(path_)
        info['base_name'] = PathManager.file_basename(path_)
        info['extension'] = PathManager.file_extension(path_)
        info['exists   '] = PathManager.exists(path_)
        info['path2file'] = PathManager.fullpath(path_)
        if prnt:
            print(json.dumps(info, indent=0))
        return info


class Folder(object):
    """Abstraction for a folder implementation. It provides a set of usable
    methods for folders.
    """
    def __init__(self, path_, absolute=True, debug=False):
        """

        :param path_:
        :param absolute:
        :param debug:
        """
        self.path = path_

        if absolute:
            self.path = self.absolute_path()

        self.content = self.get_content()
        self.paths = PathManager

    def contains(self, filename):
        """Checks if the given path is contained within the content of the
        folder

        :param filename: str: name of the file to check
        :return: bool: True if the folder contains the given file, False if not
        """
        files = self.files()
        for file in files:
            if self.paths.file_name(file) == filename:
                return True
        return False

    def join_path(self, path_):
        return PathManager.join(path_)

    def absolute_path(self):
        return os.path.abspath(self.path)

    @property
    def exists(self):
        """Asks to the OS if it is a fodler: os.path.isdir"""
        return PathManager.is_folder(self.path)

    def get_content(self, files=True, folders=True, as_class=False):
        """Return all the content of the folder considering as a root,
        it does not follows the tree
        """
        if not self.exists:
            print("Warning: Folder:" + self.path)
            print("    Folder does not exist or you have not enough "
                  "permissions to access it. Imposible to get content.")
            return []

        contents = []
        for content in os.listdir(self.path):
            content_path = PathManager.join([self.path, content])
            if files and PathManager.is_file(content_path):
                if as_class:
                    contents.append(File(content_path))
                else:
                    contents.append(content_path)
            if folders and PathManager.is_folder(content_path):
                if as_class:
                    contents.append(Folder(content_path))
                contents.append(content_path)
        return contents

    def files(self):
        return self.get_content(files=True, folders=False)

    def folders(self):
        return self.get_content(files=False, folders=True)

    def info(self, prnt=False):
        """
        Returns the basic information of the path

        :param prnt: bool: print informatin on console
        :return: dictionary with the information
        """
        info = PathManager.basic_info(self.path, prnt=False)
        content = {'folders': self.folders(), 'files  ': self.files()}
        info['content'] = content

        if prnt:
            print(json.dumps(info, indent=2))
        return info


class File(object):
    """
    Abstraction for a File implementation. It provides a set of usable methods for files.
    """
    def __init__(self, path_, relative=False, enconding=default_encoding, debug=False):

        self.paths = PathManager
        self.debug = debug

        self.folder = None
        self.name = None
        self.baseName = None
        self.extension = None
        self.content = None
        self.is_io = False
        self.encoding = enconding

        self.path = path_
        if type(path_) == str:
            self._build(path_)
        elif type(path_) == io.StringIO:
            self.is_io = True
            self.content = path_.getvalue()

    def _build(self, path_):
        if type(path_) != str:
            return

        self.is_io = False
        self.path = path_
        self.folder = self.paths.in_folder(path_)
        self.name = self.paths.file_name(path_)
        self.baseName = self.paths.file_basename(path_)
        self.extension = self.paths.file_extension(path_)
        self.content = self.read()

    @property
    def exists(self):
        """
        Asks to the OS if it is a file: os.path.isfile
        """
        if self.is_io:
            return False
        return self.paths.is_file(self.path)

    def _save(self, content):
        """
        Writes the given content (string) to the file, overrides everything inside. Default encoding utf8

        :param content: str: string to be saved
        :return: bool: True success; False: error
        """
        if self.is_io:
            return False
        try:
            FO = codecs.open(self.path, 'w', encoding=self.encoding)
            FO.write(content)
            FO.close()
            if self.debug:
                print("Done: Saved File: " + self.path)
            return True
        except IOError:
            if self.debug:
                print("Error: File not saved: " + self.path)
            return False

    def savelines(self):
        """
        Writes the given content (string) to the file, overrides everything
        inside. Default encoding utf8

        :param: lines: list: list of string to be saved
        :return: bool: True success; False: error

        """
        if self.is_io:
            return False
        elif not self.content:
            return
        self._save("\n".join(self.content))

    def update(self, content):

        if self.is_io:
            output = io.StringIO()
            output.write(content)
            # update the "path" that in this case holds the StringIO
            self.path = output
            self.content = output.getvalue()
            return
        self.content = content
        self.save()

    def save(self):
        """
        Writes the given content (string) to the file, overrides everything
        inside. Default encoding utf8

        :param: lines: list: list of string to be saved
        :return: bool: True success; False: error

        """
        self._save(self.content)

    def _read(self, as_lines):
        """
        Reads the content stored in the file

        :param as_lines: bool: If true, uses file.readlines() if not uses file.read()
        :param encoding: str: encoding to use, default 'utf8'
        :param on_error: bool: action to take in the case of an error, default ignore
        :return: lines: list of lines or single string, depending on asLines
        """
        content = None
        if self.is_io:
            return False
        try:
            file_input = codecs.open(self.path, 'r', encoding=self.encoding)
            if as_lines:
                content = file_input.readlines()
            else:
                content = file_input.read()
            file_input.close()

        except IOError:
            if self.debug:
                print("Error: File opening File: " + self.path)
        return content

    def read(self):
        """Readst he content of the file,
        """
        if self.is_io:
            return False
        return self._read(as_lines=False)

    def readlines(self):
        """
        Reads the content of the file

        :return: list
        """
        if self.is_io:
            return False
        return self._read(as_lines=True)

    def info(self, prnt=False):
        """
        Returns the basic information of the file

        :param prnt: bool: used to ptint the information on the console
        :return: dict
        """

        return self.paths.basic_info(self.path, prnt)


if __name__ == "__main__":
    pass
