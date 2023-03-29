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
`readenv.readenv.loads` will search for `.env` and `.env.local` files by default.

#### Automatic load

You can automatically load at startup time with the helper import 

```python
import readenv.loads

...
```

which try to locate and load the first env file found from your current working directory up to
root.

#### Manually load

Alternatively, you can customize which files `readenv` should search and load

```python
from readenv import readenv

readenv.loads("myenv", "myenv.local")
```

## Examples

### Django integration

Put the helper import as first place

#### `manage.py`

```python
#!/usr/bin/env python3

import readenv.loads # noqa: F401 isort:skip

import os
import sys

if  __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
```

#### `wsgi.py`

```python
import readenv.loads # noqa: F401 isort:skip

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_wsgi_application()
```

#### `asgi.py`

```python
import readenv.loads # noqa: F401 isort:skip

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_asgi_application()
```
