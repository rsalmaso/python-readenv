# python-readenv

`readenv` makes it easy to automatically load environment variables from `.env` file(s) and put into `os.environ`.

## Install

```shell
$ pip install python-readenv
```

## Getting started

You can automatically load at startup time with the helper import `import readenv.loads`,
which try to locate and load the first env file found from your current working directory up to
root.
By default it will search for `.env` and `.env.local` files.

#### Automatic load

You can automatically load at startup time with the helper import 

```python
import readenv.loads

...
```

which try to locate and load the first env file found from your current working directory up to
root.

#### Manual load

Alternatively, you can customize which files `readenv` should search and load

```python
import readenv

readenv.load("myenv", "myenv.local")
```

#### mypy integration

If you need to load the environment from mypy you could add

```ini
[mypy]
plugins = readenv.mypy
```

in your `mypy.ini` or `setup.cfg` [file](https://mypy.readthedocs.io/en/latest/config_file.html).

[pyproject.toml](https://mypy.readthedocs.io/en/stable/config_file.html#using-a-pyproject-toml-file) configuration is also supported:

```toml
[tool.mypy]
plugins = ["readenv.mypy"]
```

## Custom environment

You can create your own environment

```python
import readenv

env = readenv.Environ()
```

or start with the current environ copy

```python
import copy
import os
import readenv

env = Environ(copy.deepcopy(os.environ))
```

## Examples

### Django integration

Put the helper import as first place

#### `manage.py`

```python
#!/usr/bin/env python3

import readenv.loads  # noqa: F401 isort:skip

import sys


if __name__ == "__main__":
    readenv.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
```

#### `wsgi.py`

```python
import readenv.loads  # noqa: F401 isort:skip
from django.core.wsgi import get_wsgi_application


readenv.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
application = get_wsgi_application()
```

#### `asgi.py`

```python
import readenv.loads  # noqa: F401 isort:skip
from django.core.asgi import get_asgi_application


readenv.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
application = get_asgi_application()
```
