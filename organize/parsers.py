"""
Holds base Parser class and the parser registry of default parsers.
"""
import os.path
from organize.utils import import_class


# Generally it's better to use ``append_parsers`` or ``prepend_parsers``
# in ``Optimizer.__init__`` than to modify the default parser registry.
PARSER_REGISTRY = ['organize.csv_parser.CSVParser', 'organize.tsv_parser.CSVParser']


def registered_parsers():
    "Retrieve parser classes."
    return [import_class(x) for x in PARSER_REGISTRY]


class Parser(object):
    "Base parser class."
    mimetypes = ()
    extensions = ()

    def can_parse(self, stream):
        """
        Determine if you can read a stream,
        while reading as little as possible.

        Returns True or False

        Does not need to reset seek.
        """
        raise NotImplemented

    def parse(self, stream, columns=None):
        """
        Create a generator which transforms the stream into rows.
        
        Specifically it should yield each row as a list of
        2-tuples (column name, column value).
        """
        raise NotImplemented

    def should_parse_by_filename(self, filename):
        """
        Return whether or not the parser believes it can
        parse a file based on the file's filename.

        This is used to prioritize parsers, and will
        not prevent attempting a parser on a poorly
        labeled file.
        """
        ext = os.path.splitext(filename)[1] if filename else None
        return ext in self.extensions

    def should_parse_by_mimetype(self, mimetype):
        """
        Whether or not the parser believes it can parse
        a file based on the file's mimetype.

        This is used to prioritize parsers, and will
        not prevent attempting a parser on a poorly
        labeled file.
        """
        return mimetype in self.mimetypes
