from collections import namedtuple


FIELD_NAMES = ('index', 'subject', 'predicate', 'object', 'confidence')

class Triple(namedtuple('Triple', FIELD_NAMES)):
    def __repr__(self):
        items = [(field, getattr(self, field, None)) for field in FIELD_NAMES]
        fields = ['%s=%r' % (k, v) for k, v in items if v is not None]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(fields))


class Corpus(list):
    #def as_tsv(self):
    @classmethod
    def from_tsv(this_class, stream, print_sent_confidence):
        stream = iter(stream)
        corpus = this_class()
        for line in stream:
            if not print_sent_confidence:
                (ident, subj, pred, obj) = line.split('\t')
                triple = Triple(ident, subj.strip('"'), pred.strip('"'),
                                obj.strip('"'), None)
                corpus.append(triple)
            else:
                (ident, subj, pred, obj, conf) = line.split('\t')
                triple = Triple(ident, subj.strip('"'), pred.strip('"'),
                                obj.strip('"'), conf.strip('"'))
                corpus.append(triple)
        return corpus
