"""
Extracting documentation from python objects
"""
import inspect
import re

import attr

import ftfy


@attr.s
class Documentation(object):
    """
    A docstring parser
    """
    raw = attr.ib()
    decode = attr.ib(default=False)

    @property
    def first(self):
        return self.raw.split('\n')[0]

    @property
    def full(self):
        """
        The full docstring, line-folded
        """
        # conveniently, all these calls return unicode if they're passed in unicode, so we
        # won't mangle unicode docstrings at this point.
        out = re.sub(r'\n\n', '\v', self.raw)
        return out.replace('\n', ' ').replace('\v', '\n\n')

    @classmethod
    def fromObject(cls, obj, decode=None):
        """
        Construct a `Documentation` from any object with a docstring

        With `decode=True`, decode docstrings as utf-8, then run them through ftfy, and return unicode.
        """
        if obj.__doc__ is None:
            return cls(u'' if decode else '')
        r = cls.fromString(obj.__doc__, decode=decode)
        return r

    @classmethod
    def fromString(cls, s, decode=None):
        out = inspect.cleandoc(s)
        if not decode or isinstance(out, unicode):
            return cls(out)
        else:
            return cls(ftfy.fix_encoding(out.decode('utf-8')))


def doc(obj):
    """
    The most common case, just give me the first line
    """
    return Documentation.fromObject(obj).first
