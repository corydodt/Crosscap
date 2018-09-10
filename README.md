# Crosscap [![Build Status](https://travis-ci.org/corydodt/Crosscap.svg?branch=master)](https://travis-ci.org/corydodt/Crosscap)
Suite of tools for enhancing the Klein web framework


## Running Tests

```
$ tox
```

##  Build/upload

```
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```

## Change Log

### [0.3.0] - 2018.09.10

### Added:
  - Crosscap now fully supports Python 3.6+ (#3)

### [0.2.2] - 2018.04.17

#### Added:
  - `crosscap.testing.request()` sets a default response code of 200


### [0.2.1] - 2017.12.30

#### Fixed:
  - `urltool` is now distributed as a script


### [0.2.0] - 2017.12.30

#### Added:
  - `crosscap.testing` for testing apps that use crosscap


### [0.1.0] - 2017.12.29

#### Added:
  - Initial release


[0.3.0]: https://github.com/corydodt/Crosscap/compare/release-0.2.2...release-0.3.0
[0.2.2]: https://github.com/corydodt/Crosscap/compare/release-0.2.1...release-0.2.2
[0.2.1]: https://github.com/corydodt/Crosscap/compare/release-0.2.0...release-0.2.1
[0.2.0]: https://github.com/corydodt/Crosscap/compare/release-0.1.0...release-0.2.0
[0.1.0]: https://github.com/corydodt/Crosscap/tree/release-0.1.0
