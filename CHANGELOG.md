# Changelog

## dev

* update ruff to 0.11.2
* switch development to uv/nox[uv] and replace custom requirements with uv.lock file
* upgrade all requirements to latest version

## 0.7.0

* made dict converter separators customizable
* EXPERIMENTAL: made the json converter aware of base64 content
  and automatically decode it

## 0.6.1

* added nox
* commit tests

## 0.6.0

* BREAKING: don't override existing enviroment values
* updated typing

## 0.5.0

* added py.typed marker
* added mypy pluging

## 0.4.0

* add separator parameter to Environ.list
* add cast parameter to Environ.list
* add separator to Environ.tuple
* add cast parameter to Environ.tuple

## 0.3.1

* always apply cast

## 0.3.0

this is a refactor release

* refactored code: added Environ class

## 0.2.0

* fix typing support for python 3.8
* made `readenv.redenv.load` "private" (`readenv.readenv._load`)
* rename `readenv.readenv.loads` to `readenv.readenv.load`
* export `readenv.readenv.load` as `readenv.load`
* added `readenv.env.get`, `readenv.env.set`, and `readenv.env.setdefault`,
  and exported to `readenv`
* added type converters

## 0.1.1

* can pass env absolute path

## 0.1.0

* first public release
