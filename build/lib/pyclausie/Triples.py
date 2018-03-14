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

from collections import namedtuple


FIELD_NAMES = ('index', 'subject', 'predicate', 'object', 'confidence')

class Triple(namedtuple('Triple', FIELD_NAMES)):
    """ Inherits from namedtuple. This tuple contains the fields index,
        subject, predicate, object, and confidence.
    """
    def __repr__(self):
        items = [(field, getattr(self, field, None)) for field in FIELD_NAMES]
        fields = ['%s=%r' % (k, v) for k, v in items if v is not None]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(fields))


class Corpus(list):
    """ Inherits from list. Corpus parses the ClausIE output and stores
        a list of Triple.
    """
    #def as_tsv(self):
    @classmethod
    def from_tsv(this_class, stream, print_sent_confidence):
        stream = iter(stream)
        corpus = this_class()
        for line in stream:
            if not print_sent_confidence:
                (ident, subj, pred, obj) = line.decode().split('\t')
                triple = Triple(ident, subj.strip('"'), pred.strip('"'),
                                obj.strip('"'), None)
                corpus.append(triple)
            else:
                (ident, subj, pred, obj, conf) = line.decode().split('\t')
                triple = Triple(ident, subj.strip('"'), pred.strip('"'),
                                obj.strip('"'), conf.strip('"'))
                corpus.append(triple)
        return corpus
