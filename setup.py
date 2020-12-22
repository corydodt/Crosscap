from inspect import cleandoc

from setuptools import setup, find_packages


__version__ = '0.5.0'


cfg = dict(
    name = 'Crosscap',
    packages=find_packages('.', include=['crosscap', 'crosscap.*']),
    version = __version__,
    description = 'Suite of tools for enhancing the Klein web framework',
    author = 'Cory Dodt',
    author_email = 'corydodt@gmail.com',
    url = 'https://github.com/corydodt/Crosscap',
    keywords = [],
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    scripts = ['bin/urltool'],
    extras_require={
        # tests
        'dev': [
            "pytest-cov",
            "pytest-twisted",
            "pytest",
            'mock',
            'pyflakes',
            'pytest-flakes',
            'pytz',
            'tox',
        ],
    },
    install_requires=cleandoc('''
        click>=6.7
        ftfy==4.4.3;python_version<'3'
        ftfy;python_version>='3'
        future>=0.16.0
        klein
        pyjwt>=1.7.1
        pyyaml>=3.12
        twisted>=17.1.0
        werkzeug>=0.13
        wrapt>=1.11.1
        ''').split(),
    zip_safe=False,
)

setup(**cfg)
