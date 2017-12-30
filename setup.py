from inspect import cleandoc

from setuptools import setup

_version = {}
execfile('crosscap/_version.py', _version)

setup(
    name = 'Crosscap',
    packages = ['crosscap',],
    version = _version['__version__'],
    description = 'idk fix later',
    author = 'Bright.md',
    author_email = 'cory@bright.md',
    url = 'https://github.com/corydodt/Crosscap',
    keywords = [],
    classifiers = [],
    scripts = [],
    install_requires=cleandoc('''
        attrs
        ''').split()
)
