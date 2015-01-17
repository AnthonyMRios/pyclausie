import os
import subprocess
import tempfile
from .ClausIE import ClausIE
from .Triples import Corpus

class SubprocessBackend(ClausIE):
    def __init__(self, jar_filename=None, download_if_missing=False,
                 version=None, java_command='java'):
        ClausIE.__init__(self, jar_filename, download_if_missing,
                         version)
        self.java_command = java_command
    
    def extract_triples(self, sentences, ids=None, java='java',
                        print_sent_confidence=False):
        input_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            if ids is not None:
                for identifier, sentence in zip(ids, sentences):
                    input_file.write('%r\t%r\n' % (identifier, sentence))
            else:
                for sentence in sentences:
                    input_file.write('%r\n' % sentence)
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
            print 'stderr:', stderr
            raise ValueError("Bad exit code from ClausIE.")
