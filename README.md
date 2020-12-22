# Crosscap [![Build Status](https://travis-ci.org/corydodt/Crosscap.svg?branch=master)](https://travis-ci.org/corydodt/Crosscap)
Suite of tools for enhancing the Klein web framework


## Running Tests

```
$ tox
```

##  Build/upload

- Update setup.py with a new version
- Update the Change Log below
- **Commit your changes to the above files.**
- Add and push a tag for the new release

```
$ python3 setup.py sdist bdist_wheel && python2 setup.py bdist_wheel
$ twine upload dist/*
```

For point releases: Make sure there is a `series-0.x` branch in github, and branch from that branch.

## Change Log

### [0.5.0] - 2020.12.22

### Fixed:
  - Pyyaml 5.x now supported

### [0.4.9] - 2019.07.23

### Fixed:
  - We don't need to specify pytest stuff in our hard dependencies; move them into [dev] dependencies

### [0.4.4] - 2019.06.07

### Fixed:
  - `permits()` decorator uses a more robust method of looking for the request handler in the args of the function it's decorating, now applies
    to more use cases.
  - actually include the permitting package in the distribution of crosscap

### [0.4.2] - 2019.05.31

### Changed:
  - `crosscap.permitting.validate_token` now returns the entire payload, and has a default return parameter so you can choose what you'll get back.

### [0.4.0] - 2019.05.30

### Added:
  - `crosscap.permitting`, an API for adding authorization to your request handlers (see doc/example/permitting)

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


[0.5.0]: https://github.com/corydodt/Crosscap/compare/release-0.4.9...release-0.5.0
[0.4.9]: https://github.com/corydodt/Crosscap/compare/release-0.4.4...release-0.4.9
[0.4.4]: https://github.com/corydodt/Crosscap/compare/release-0.4.2...release-0.4.4
[0.4.2]: https://github.com/corydodt/Crosscap/compare/release-0.4.0...release-0.4.2
[0.4.0]: https://github.com/corydodt/Crosscap/compare/release-0.3.0...release-0.4.0
[0.3.0]: https://github.com/corydodt/Crosscap/compare/release-0.2.2...release-0.3.0
[0.2.2]: https://github.com/corydodt/Crosscap/compare/release-0.2.1...release-0.2.2
[0.2.1]: https://github.com/corydodt/Crosscap/compare/release-0.2.0...release-0.2.1
[0.2.0]: https://github.com/corydodt/Crosscap/compare/release-0.1.0...release-0.2.0
[0.1.0]: https://github.com/corydodt/Crosscap/tree/release-0.1.0
