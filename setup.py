from inspect import cleandoc

from setuptools import setup

_version = {}
execfile('crosscap/_version.py', _version)

setup(
    name = 'Crosscap',
    packages = ['crosscap',],
    version = _version['__version__'],
    description = 'idk fix later',
    author = 'Cory Dodt',
    author_email = 'corydodt@gmail.com',
    url = 'https://github.com/corydodt/Crosscap',
    keywords = [],
    classifiers = [],
    scripts = ['bin/urltool'],
    install_requires=cleandoc('''
        click>=6.7
        ftfy==4.4.3
        pytest>=3.1.0
        pytest-cov>=2.5.1
        pytest-flakes>=2.0.0
        pytest-twisted>=1.5
        pyyaml>=3.12,<4.0
        twisted>=17.1.0
        werkzeug>=0.13
        ''').split()
)
