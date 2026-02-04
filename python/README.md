# Python

1. [TL;DR](#tldr)
1. [Learning material](#learning-material)
1. [Virtual environments](#virtual-environments)
   1. [Creating virtual environments](#creating-virtual-environments)
   1. [Activating virtual environments](#activating-virtual-environments)
   1. [Installing packages in virtual environments](#installing-packages-in-virtual-environments)
   1. [Managing virtual environments](#managing-virtual-environments)
1. [Modules of interest](#modules-of-interest)
1. [Parallelization](#parallelization)
1. [Packaging](#packaging)
1. [Plugin systems](#plugin-systems)
   1. [Self-registration via decorator](#self-registration-via-decorator)
1. [Further readings](#further-readings)
   1. [Sources](#sources)

## TL;DR

Prefer giving each project its own private [virtual environment][virtual environments].

```py
# Built-in types
boolean_value = True
boolean_value = False
integer_value = 1000000
integer_value = 1_000_000
floating_point_value = 2.8
complex_value = 1j
string_value = 'some value'
string_value = "some other value"
a_list = ['apple', 'banana', 'cherry', 7, True]
a_tuple = ("apple", "banana", "cherry", 42, False)  # ordered, unchangeable list
a_set = {"apple", "banana", "cherry", 42, False}    # unordered, non-indexed collection of unchangeable items
a_dictionary = {                                    # ordered (since v3.7) collection of non-duplicable key:value pairs
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
a_dictionary = dict(
    name = "John",
    age = 36,
    country = "Norway",
)

# Get variables' type
type(True)           # -> <class 'bool'>
type(1000000)        # -> <class 'int'>
type(1_000_000)      # -> <class 'int'>
type(2.8)            # -> <class 'float'>
type(1j)             # -> <class 'complex'>
type('some string')  # -> <class 'str'>
type([])             # -> <class 'list'>
type(set())          # -> <class 'set'>
type({})             # -> <class 'dict'>
type(tuple())        # -> <class 'tuple'>

# Convert between types
bool('some string')                   # -> True
bool(0)                               # -> False
int(2.8)                              # -> 2
int('10')                             # -> 10
float(28)                             # -> 28.0
float('42')                           # -> 42.0
complex(21)                           # -> (2+0j)
str(False)                            # -> 'False'
str(1)                                # -> '1'
list(("apple", "banana", "cherry"))   # -> ['apple', 'banana', 'cherry']
tuple(["apple", "banana", "cherry"])  # -> ('apple', 'banana', 'cherry')
set(['banana', 'cherry', 'apple'])    # -> {'banana', 'cherry', 'apple'}
tuple({"some": "dict"})               # -> ('some',)
set({"some": "dict"})                 # -> {'some'}

# Get lengths
print(len(a_list))
print(len(a_dict))

# Unset variables
kwargs = None  # deletes the value, and lets the garbage collector take care of memory from here
del kwargs     # deletes the variable's reference immediately

# Ask users for input
print("Enter your name:")
name = input()
print(f"Hello {name}")

# Sort lists
orig_list.sort(key=lambda x: x.count, reverse=True)                # sort in place
new_list = sorted(orig_list, key=lambda x: x.count, reverse=True)  # return a new, sorted list

# Convert lists to sets
# by using the set() function
custom_list = set(custom_list)
print(f'type: {type(custom_list)}, content: {custom_list}')
# by unpacking the list's items to form the set
custom_list = {*custom_list}
print(f'type: {type(custom_list)}, content: {custom_list}')

# Check a dictionary contains a key
if 'key_name' in dictionary: pass

# Provide a default value when a key does not exist in a dictionary
dictionary.get('key_name', 42)

# Check if a dictionary is subset of another
whole =  { 'greg': 1, 'knows': 2, 'what': 3, 'is': 4, 'best': 5, 'for': 6, 'himself': 7 }
part = { 'greg': 1, 'knows': 2, 'himself': 7}
part_is_subset_of_whole = part.items() <= whole.items()

# Show available (imported and built-in) modules
print(globals())
print(locals())

# Check a module is imported
'os' in globals()

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
# returns a match object that can be used in conditionals (evaluates True if matched)
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
def format_phone_number(phone: str|None) -> None: pass                 # since python 3.10
```

Generally:

- `map()` =~ plain `for` loop =~ operation in constructor performance-wise.

  <details style='padding: 0 0 1rem 1rem'>

  See [When should I use a Map instead of a For Loop?].

  ```sh
  # tested with 3.11 and 3.12
  $ python3 'experiments/performance-measuring.py'
  plain for loop: 2.755201207997743
  list constructor: 2.8492380419920664
  map: 2.7811154999944847
  ```

  </details>

## Learning material

- W3C's [Python tutorial][w3c python tutorial]

Fast-track:

1. Learn Object-Oriented Programming's basic concepts.
1. Read code made by others.<br/>
   Goal: understand the code.
1. Reimplement or improve existing pieces of code.<br/>
   Goal: understand the reasoning behind the code.
1. Create small utilities for yourself.
1. Grow your code in complexity.

## Virtual environments

Most Python's package management implementations suck, and create conflicts with each other.

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

> [!tip]
> Prefer giving each project its own private [virtual environment][virtual environments].

### Creating virtual environments

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

### Activating virtual environments

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

### Installing packages in virtual environments

```sh
source '.venv/bin/activate' && python3 -m pip install --requirement 'requirements.txt'
.venv/bin/pip3 --require-virtualenv install -r 'requirements.txt' --dry-run
```

### Managing virtual environments

```sh
# Get installed packages with version.
python3 -m pip freeze
pip freeze > 'requirements.txt'

# Upgrade packages.
sed -e 's/^#.*$//' -e 's/==/>=/' 'requirements.txt' | xargs .venv/bin/pip --require-virtualenv install --upgrade
pip freeze | sed 's/==/>=/' | xargs pip --require-virtualenv install --upgrade
```

## Modules of interest

| Module               | Use cases                                                                |
| -------------------- | ------------------------------------------------------------------------ |
| [bitmath]            | Interact with file sizes in various units                                |
| [boto3]              | Interact with AWS services                                               |
| [ciso8601]           | Convert ISO8601 or RFC3339 datetime strings into Python datetime objects |
| [concurrent.futures] | Parallelization                                                          |
| [dask]               | Parallel and distributed computing                                       |
| [logging]            | Logging                                                                  |
| [mypy]               | Static type checking                                                     |
| [playwright]         | Automate browser windows                                                 |
| [psycopg]            | Interact with PostgreSQL databases                                       |
| [selenium]           | Automate browser windows                                                 |
| [tabulate]           | Pretty-print tabular data                                                |
| [tqdm]               | Simplified threading with progress bars                                  |
| [typer]              | CLI applications                                                         |

## Parallelization

TODO

Refer [concurrent.futures] and [tqdm].<br/>
See also [Using tqdm with concurrent.futures in Python].

## Packaging

TODO

## Plugin systems

### Self-registration via decorator

Plugins manage themselves.<br/>
Adding a new plugin is just a matter of dropping in a `.py` file using a decorated function.<br/>
No need to manually update lists or registries.

See the [experiment](./experiments/plugin_systems/self-registration_via_decorator/README.md).

## Further readings

- [Using tabulation in Python logging format]
- [Python Virtual Environments: A Primer]
- [mypy documentation]

### Sources

- [venv — creation of virtual environments]
- [Install packages in a virtual environment using pip and venv]
- [Python module import: single-line vs multi-line]
- [Convert List to Set]
- [When should I use a Map instead of a For Loop?]
- [Python 3 type hinting for None?]
- [How to specify multiple return types using type-hints]
- [Using tqdm with concurrent.futures in Python]
- [Check if one dictionary is subset of other]
- [Python void return type annotation]
- [Type hints cheat sheet]
- [Namespaces in Python]

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
[bitmath]: https://bitmath.readthedocs.io/en/latest/module.html
[boto3]: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
[check if one dictionary is subset of other]: https://www.geeksforgeeks.org/python-check-if-one-dictionary-is-subset-of-other/
[ciso8601]: https://pypi.org/project/ciso8601/
[concurrent.futures]: https://docs.python.org/3/library/concurrent.futures.html
[convert list to set]: https://pythonexamples.org/python-convert-list-to-set/
[dask]: https://www.dask.org/
[how to specify multiple return types using type-hints]: https://stackoverflow.com/questions/33945261/how-to-specify-multiple-return-types-using-type-hints
[logging]: https://docs.python.org/3/library/logging.html
[mypy documentation]: https://mypy.readthedocs.io/en/stable/
[mypy]: https://github.com/python/mypy
[Namespaces in Python]: https://realpython.com/python-namespace/
[playwright]: https://playwright.dev/python/
[psycopg]: https://www.psycopg.org/
[python 3 type hinting for none?]: https://stackoverflow.com/questions/19202633/python-3-type-hinting-for-none
[python module import: single-line vs multi-line]: https://stackoverflow.com/questions/15011367/python-module-import-single-line-vs-multi-line
[python virtual environments: a primer]: https://realpython.com/python-virtual-environments-a-primer/
[Python void return type annotation]: https://stackoverflow.com/questions/36797282/python-void-return-type-annotation
[selenium]: https://pypi.org/project/selenium/
[tabulate]: https://pypi.org/project/tabulate/
[tqdm]: https://tqdm.github.io/
[Type hints cheat sheet]: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
[typer]: https://github.com/fastapi/typer
[using tabulation in python logging format]: https://stackoverflow.com/questions/2777169/using-tabulation-in-python-logging-format#26145642
[using tqdm with concurrent.futures in python]: https://rednafi.com/python/tqdm_progressbar_with_concurrent_futures/
[w3c python tutorial]: https://www.w3schools.com/python
[when should i use a map instead of a for loop?]: https://stackoverflow.com/questions/1975250/when-should-i-use-a-map-instead-of-a-for-loop
