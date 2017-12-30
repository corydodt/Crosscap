"""
Tests of the doc class
"""
from crosscap import doc

def test_doc():
    """
    Does the doc function return the first line?
    """
    def aFunction(): # pragma: nocover
        """
        Hello

        there
        """

    assert doc.doc(aFunction) == "Hello"
