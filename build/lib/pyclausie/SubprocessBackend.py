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

import os
import subprocess
import tempfile
from .ClausIE import ClausIE
from .Triples import Corpus

class SubprocessBackend(ClausIE):
    """ Interface to ClausIE using subprocess. This creates a java call
        to clausie.jar.
    """
    def __init__(self, jar_filename=None, download_if_missing=False,
                 version=None, java_command='java'):
        """ java_command is the path the the java binary.
        """
        ClausIE.__init__(self, jar_filename, download_if_missing,
                         version)
        self.java_command = java_command
    
    def extract_triples(self, sentences, ids=None, java='java',
                        print_sent_confidence=False):
        """ This method takes a list of sentences and ids (optional)
            then returns a list of triples extracted by ClausIE.

            currently supported options:
                -l - Used if ids is a list and not None.
                -p - Returns the confidence score of the extracted
                     triple.
            
            Note: sentences and ids must be a list even if you only
                  extract triples for one sentence.
        """
        input_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            if ids is not None:
                for identifier, sentence in zip(ids, sentences):
                    input_file.write('{0!r}\t{1!r}\n'.format(identifier, sentence).encode('utf8'))
            else:
                for sentence in sentences:
                    input_file.write('{0!r}\n'.format(sentence).encode('utf8'))
            input_file.flush()

            command = [self.java_command,
                       '-jar', self.jar_filename,
                       '-f', input_file.name]
            if ids is not None:
                command.append('-l')
            if print_sent_confidence:
                command.append('-p')
            sd_process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
            return_code = sd_process.wait()
            stderr = sd_process.stderr.read()
            stdout = sd_process.stdout.read()
            self._raise_on_bad_exitcode(return_code, stderr)
        finally:
            os.remove(input_file.name)
        
        triples = Corpus.from_tsv(stdout.splitlines(), print_sent_confidence)
        return triples

    @staticmethod
    def _raise_on_bad_exitcode(return_code, stderr):
        if return_code:
            print('stderr:', stderr)
            raise ValueError("Bad exit code from ClausIE.")
