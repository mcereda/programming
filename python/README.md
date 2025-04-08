# Python

1. [TL;DR](#tldr)
1. [Modules of interest](#modules-of-interest)
1. [Parallelization](#parallelization)
1. [Virtual environments](#virtual-environments)
   1. [Create virtual environments](#create-virtual-environments)
   1. [Activate virtual environments](#activate-virtual-environments)
   1. [Install packages in virtual environments](#install-packages-in-virtual-environments)
   1. [Manage virtual environments](#manage-virtual-environments)
1. [Further readings](#further-readings)
   1. [Sources](#sources)

## TL;DR

Use a [virtual environment][virtual environments] for each project.

```py
custom_list = ['apple', 'banana', 'cherry']
custom_dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# Get lengths
print(len(custom_list))
print(len(custom_dict))

# Unset variables
# By deleting their value and letting the garbage collector take care of it
kwargs = None
# By deleting their reference
del kwargs

# Convert lists to sets
# By using the set() function
custom_list = set(custom_list)
print(f'type: {type(custom_list)}, content: {custom_list}')
# By unpacking the list's items to form the set
custom_list = {*custom_list}
print(f'type: {type(custom_list)}, content: {custom_list}')

# Convert dictionaries to tuples
# By using the tuple() function
custom_dict = tuple(custom_dict)

# Check if one dictionary is subset of another
whole =  { 'greg': 1, 'knows': 2, 'what': 3, 'is': 4, 'best': 5, 'for': 6, 'himself': 7 }
part = { 'greg': 1, 'knows': 2, 'himself': 7}
part_is_subset_of_whole = part.items() <= whole.items()

# Get values from environment variables
import os
print(os.environ('HOME'))
print(os.environ.get('LOG_LEVEL', default=logging.INFO))
print(os.getenv('GITLAB_TOKEN'))
print(os.getenv('AWS_PROFILE', default='default'))

# Define functions
def function_name(): pass
def function_with_arguments(arg1, arg2 = None): pass
def function_with_type_hinting(arg1: str, arg2: bool | None = False) -> str | None: pass  # from 3.10

# Get function name from inside them
def function_using_inspect():
    import inspect
    print(inspect.stack()[0][3])  # -> 'function_using_inspect'
def function_using_sys():
    import sys
    print(sys._getframe().f_code.co_name)  # -> 'function_using_sys'

# Set logging per function
def function_with_logging( log_level: str = 'WARN' ) -> None:
    import logging
    import sys

    logger = logging.getLogger(sys._getframe().f_code.co_name)
    logger.setLevel(logging.getLevelName(log_level.upper()))
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug(vars())

# `except` clauses may name multiple exceptions as a parenthesized tuple
try: pass
except (IDontLikeYouException, YouAreBeingMeanException) as e: raise
```

Work with regular expressions:

```py
import re

# Just check for matches
# Returns a match object that can be used in conditionals (evaluates True if matched)
re.match(r".* something .*", 'find if something matches')

# Parse
pattern = re.compile(r'^(?P<source>\d+|NOT_FOUND)-(?P<destination>\d+|NOT_FOUND)-(?P<timestampz>\d+(.\d+)?).ogg$')
matches = pattern.match('000000000-000000000-0000000000.00000.ogg')
source = matches.group('source')
destination = matches.group('destination')
timestamp = datetime.fromtimestamp(float(matches.group('timestampz')), timezone.utc)

# Replace text
source_intl = re.sub(r'^\+?(39)?(?P<phoneNum>(0|2)\d+)', r'+39\g<phoneNum>', source) if source is not None else source
```

Type hinting (since Python 3.5):

```py
dry_run: bool = True
processed: int = 0
source_name: str = 'test'
def format_phone_number_old(phone: typing.Optional[str] = None): pass  # python 3.5 to 3.10
def format_phone_number(phone: str|None) -> None: pass  # since python 3.10
```

Generally:

- `map()` =~ plain `for` loop =~ operation in constructor performance-wise.

  <details>
    <summary>Reasoning</summary>

  See [When should I use a Map instead of a For Loop?].

  ```sh
  # tested with 3.11 and 3.12
  $ python3 'experiments/performance-measuring.py'
  plain for loop: 2.755201207997743
  list constructor: 2.8492380419920664
  map: 2.7811154999944847
  ```

  </details>

## Modules of interest

| Module               | Use for                                                                  |
| -------------------- | ------------------------------------------------------------------------ |
| [boto3]              | Interact with AWS services                                               |
| [ciso8601]           | Convert ISO8601 or RFC3339 datetime strings into Python datetime objects |
| [concurrent.futures] | Parallelization                                                          |
| [logging]            | Kinda self-explanatory, isn't it?                                        |
| [psycopg]            | Interact with PostgreSQL databases                                       |
| [tqdm]               | Simplified threading with progress bars                                  |

## Parallelization

TODO

Refer [concurrent.futures] and [tqdm].<br/>
See also [Using tqdm with concurrent.futures in Python].

## Virtual environments

Python's package management implementations suck and create conflicts with each other.

Virtual environments allow managing dependencies separately for different projects.<br/>
This prevents conflicts and helps maintaining cleaner setups.

Specifically, they:

- Store a specific Python interpreter version, with the libraries and binaries needed to support a project.<br/>
  These are, by default, **isolated** from software in other virtual environments as well as Python interpreters and
  libraries installed in the hosting operating system.
- Are contained to a directory.<br/>
  This directory is conventionally named `.venv` or `venv` and is stored in the project's root directory.
- Are preferably **ignored** by source control systems such as `git`.
- Are considered **disposable** — delete and recreate them any time from scratch.
- Are **not** considered movable or copyable — just recreate the virtual environment in the target location.
- Should **not** contain any project-related code.

### Create virtual environments

Leverage the `venv` module to create virtual environments.

```sh
python3 -m 'venv' '.venv'
python3.12 -m 'venv' 'venv'
```

This:

1. Creates the directory containing the environment.<br/>
   Parent directories are created as needed.
1. Places a `pyvenv.cfg` file in the environment's directory, with the `home` key pointing to the Python installation
   used to create the environment.
1. Creates a `bin` (`Scripts` on Windows) subdirectory, containing a copy (or symlink) of the Python executable.
1. Creates a `lib/pythonX.Y/site-packages` subdirectory (`Libsite-packages` on Windows).
1. Invokes `ensurepip` to bootstrap `pip` into the virtual environment, unless the `--without-pip` option is given.

If the virtual environment's directory already exists, it will be re-used.<br/>
If multiple paths are given in input, it will create identical virtual environments at **each** provided path.

### Activate virtual environments

When running from a virtual environment, a Python interpreter's `sys.prefix` and `sys.exec_prefix` will point to the
directories of the virtual environment.<br/>
`sys.base_prefix` and `sys.base_exec_prefix` will point instead to the paths of the Python interpreter used to create
the environment.

Check `sys.prefix != sys.base_prefix` to determine if the current interpreter is running from a virtual environment.

Virtual environments may be _activated_ using platform-specific scripts in their binary directory (`bin` on POSIX,
`Scripts` on Windows).<br/>
The script will **prepend** the virtual environment's binary directory to the user's PATH. From there on, running the
`python` command will invoke **the environment's** Python interpreter.

```sh
source '.venv/bin/activate'
source '.venv/bin/activate.fish'
```

One is **not** _required_ to activate virtual environments to use them.<br/>
Instead, one can just _specify the path to that environment's Python interpreter_ when invoking Python commands:

```sh
.venv/bin/pip --require-virtualenv install -r 'requirements.txt'
.venv/bin/python3 'app.py'
```

Deactivate virtual environments by executing `deactivate`.<br/>
The exact mechanism is platform-specific and is an internal implementation detail. Like activation, a script or shell
function will be used for this.

### Install packages in virtual environments

```sh
source '.venv/bin/activate' && python3 -m pip install --requirement 'requirements.txt'
.venv/bin/pip3 --require-virtualenv install -r 'requirements.txt' --dry-run
```

### Manage virtual environments

```sh
# Get installed packages with version.
python3 -m pip freeze
pip freeze > 'requirements.txt'

# Upgrade packages.
sed -e 's/^#.*$//' -e 's/==/>=/' 'requirements.txt' | xargs .venv/bin/pip --require-virtualenv install --upgrade
pip freeze | sed 's/==/>=/' | xargs pip --require-virtualenv install --upgrade
```

## Further readings

- [Using tabulation in Python logging format]
- [Python Virtual Environments: A Primer]

### Sources

- [venv — creation of virtual environments]
- [Install packages in a virtual environment using pip and venv]
- [Python module import: single-line vs multi-line]
- [Python tutorial]
- [Convert List to Set]
- [When should I use a Map instead of a For Loop?]
- [Python 3 type hinting for None?]
- [How to specify multiple return types using type-hints]
- [Using tqdm with concurrent.futures in Python]
- [Check if one dictionary is subset of other]

<!--
  Reference
  ═╬═Time══
  -->

<!-- In-article sections -->
[virtual environments]: #virtual-environments

<!-- Upstream -->
[install packages in a virtual environment using pip and venv]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
[venv — creation of virtual environments]: https://docs.python.org/3/library/venv.html

<!-- Others -->
[boto3]: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
[check if one dictionary is subset of other]: https://www.geeksforgeeks.org/python-check-if-one-dictionary-is-subset-of-other/
[ciso8601]: https://pypi.org/project/ciso8601/
[concurrent.futures]: https://docs.python.org/3/library/concurrent.futures.html
[convert list to set]: https://pythonexamples.org/python-convert-list-to-set/
[how to specify multiple return types using type-hints]: https://stackoverflow.com/questions/33945261/how-to-specify-multiple-return-types-using-type-hints
[logging]: https://docs.python.org/3/library/logging.html
[psycopg]: https://www.psycopg.org/
[python 3 type hinting for none?]: https://stackoverflow.com/questions/19202633/python-3-type-hinting-for-none
[python module import: single-line vs multi-line]: https://stackoverflow.com/questions/15011367/python-module-import-single-line-vs-multi-line
[python tutorial]: https://www.w3schools.com/python
[python virtual environments: a primer]: https://realpython.com/python-virtual-environments-a-primer/
[tqdm]: https://tqdm.github.io/
[using tabulation in python logging format]: https://stackoverflow.com/questions/2777169/using-tabulation-in-python-logging-format#26145642
[using tqdm with concurrent.futures in python]: https://rednafi.com/python/tqdm_progressbar_with_concurrent_futures/
[when should i use a map instead of a for loop?]: https://stackoverflow.com/questions/1975250/when-should-i-use-a-map-instead-of-a-for-loop
