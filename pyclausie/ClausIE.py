# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import urllib
import urllib.request
import os
import os.path
import zipfile

DEFAULT_CLAUSIE_VERSION = '0-0-1'

INSTALL_DIR = '~/.local/share/pyclausie/'

class ClausIE:
    """ This is an abstract base class for extracting triples from a
        sentence using ClausIE. To use this, you'll need to instantiate
        one of the backends. You can do this via the get_instance()
        helper method.

        If you don't have the needed clausie jar file the flag
        download_if_missing will fetch it for you.

        Subclasses need to override the extract_triples method.
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, jar_filename=None, download_if_missing=False,
                 version=None):
        """ jar_filename should point to calusie.jar. If you don't
            have this jar file the download_if_missing parameter can
            be set which will retrieve the file for you.
        """
        if not (jar_filename is not None or download_if_missing):
            raise ValueError("Must set either jar_filename or "
                             " download_if_missing to True.")

        self.jar_filename = jar_filename
        if self.jar_filename is None:
            if version is None:
                version = DEFAULT_CLAUSIE_VERSION
            filename = 'clausie/clausie.jar'
            self.jar_filename = self.setup_and_get_default_path(filename)
            if download_if_missing:
                self.download_if_missing(version)

    @abc.abstractmethod
    def extract_triples(self, sentences, ids=None, **kwargs):
        """ extract triples from list of sentences."""

    def setup_and_get_default_path(self, jar_base_filename):
        install_dir = os.path.expanduser(INSTALL_DIR)
        try:
            os.makedirs(install_dir)
        except OSError:
            pass
        jar_filename = os.path.join(install_dir, jar_base_filename)
        return jar_filename

    def download_if_missing(self, version=None, verbose=True):
        """ This method will download and extract the clausie zip
            file if it does not already exist.
        """
        if os.path.exists(self.jar_filename):
            return

        jar_url = self.get_jar_url(version)
        filename = 'clausie-%s.zip' % version
        install_dir = os.path.expanduser(INSTALL_DIR)
        zip_filename = os.path.join(install_dir, filename)
        if verbose:
            print("Downloading %r -> %r" % (jar_url, zip_filename))
        opener = ErrorAwareURLOpener()
        opener.retrieve(jar_url, filename=zip_filename)
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            zip_file.extractall(install_dir)

    @staticmethod
    def get_jar_url(version=None):
        if version is None:
            version = DEFAULT_CLAUSIE_VERSION 
        if not isinstance(version, str):
            raise TypeError("Version must be a string or None (got %r)." %
                            version)
        filename = 'clausie-%s.zip' % version
        return 'http://resources.mpi-inf.mpg.de/d5/clausie/' \
                '%s' % filename

    @staticmethod
    def get_instance(jar_filename=None, version=None,
                     download_if_missing=True, backend='subprocess',
                     **extra_args):
        extra_args.update(jar_filename=jar_filename,
                          download_if_missing=download_if_missing,
                          version=version)

        if backend == 'subprocess':
            from .SubprocessBackend import SubprocessBackend
            return SubprocessBackend(**extra_args)

        raise ValueError("Unknown backend: %r (known backends: "
                         "'subprocess')" % backend)

class ErrorAwareURLOpener(urllib.request.FancyURLopener):
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        raise ValueError("Error downloading %r: %s %s" %
                         (url, errcode, errmsg))
