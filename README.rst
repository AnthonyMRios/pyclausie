pyclausie
=========

Python wrapper around
`ClausIE <http://www.mpi-inf.mpg.de/departments/databases-and-information-systems/software/clausie/>`_.
This will take a list of sentences and return a list of triples.

How to Install
--------------

>>> python setup.py install

Example Usage
-------------

To start you must create a ClausIE instance from the pyclausie package.
::
    >>> from pyclausie import ClausIE
    >>> cl = ClausIE.get_instance()

``get_instance()`` will automatically download the clausie jar file.
If you have an existing clausie jar file you can specifiy the file
using the jar_filename parameter.

To extract triples from a sentence use the ``extract_triples()``
method. This method takes a list of sentences as input and will return
a list of Triple objects.
::
    >>> sents = ['I learned that the 2012 Sasquatch music festival is '
    ...          'scheduled for May 25th until May 28.']
    >>> triples = cl.extract_triples(sents)
    >>> for triple in triples:
    ...     print triple
    Triple(index='1', subject='I', predicate='learned', object='that the 2012 Sasquatch music festival is scheduled for May 25th until May 28')
    Triple(index='1', subject='the 2012 Sasquatch music festival', predicate='is scheduled', object='for May 25th until May 28')
    Triple(index='1', subject='the 2012 Sasquatch music festival', predicate='is scheduled', object='for May 25th')

This shows three triples returned by clausie for the given sentence.
If you wish to get the confidence score you should pass the parameter
``print_sent_confidence=True`` to the ``extract_triples()`` method.

More Information
----------------

Licensed under `Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.

Written by Anthony Rios
