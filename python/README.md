# Python

1. [TL;DR](#tldr)
1. [Learning material](#learning-material)
1. [Virtual environments](#virtual-environments)
   1. [Creating virtual environments](#creating-virtual-environments)
   1. [Activating virtual environments](#activating-virtual-environments)
   1. [Installing packages in virtual environments](#installing-packages-in-virtual-environments)
   1. [Managing virtual environments](#managing-virtual-environments)
1. [Modules of interest](#modules-of-interest)
1. [Performances](#performances)
   1. [Parallelizing tasks](#parallelizing-tasks)
   1. [Lazy formatting](#lazy-formatting)
1. [Plugin systems](#plugin-systems)
   1. [Self-registration via decorator](#self-registration-via-decorator)
1. [Packaging applications](#packaging-applications)
1. [Further readings](#further-readings)
   1. [Sources](#sources)

## TL;DR

Object-oriented programming language. Everything in Python is an _object_.<br/>
Objects are instances of what _classes_ define.

`#` starts a comment from that point to the end of the line.<br/>
`"""` start and close string literals. Standalone string literals are commonly used for multiline comments and
documentation.

<details style='padding: 0 0 1rem 1rem'>

```py
# this only lasts one line

"""
use standalone string literals for multiline comments
mostly suited for documentation
"""
```

</details>

The syntax offers some _built-in types_.<br/>
One can create new types by defining a new class for it.

<details style='padding: 0 0 1rem 1rem'>

| Type           | Key       | Summary                                                                         | Examples                                                   |
| -------------- | --------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Null/None      | `None`    | Absence of a value                                                              | `None`                                                     |
| Boolean        | `bool`    | Value that can be considered only true or false                                 | `True`, `False`                                            |
| Text/String    | `str`     | Sequence of characters                                                          | `'some value'`, `"some other value"`                       |
| Integer        | `int`     | Whole number                                                                    | `1`, `-50`                                                 |
| Floating point | `float`   | Number with a decimal point                                                     | `2.8`                                                      |
| Complex        | `complex` | Number with a real and an imaginary part                                        | `1j`                                                       |
| List           | `list`    | Ordered sequence of items                                                       | `['apple', 'banana', 'cherry', 7, True]`                   |
| Tuple          | `tuple`   | Ordered, immutable sequence of items                                            | `("apple", "banana", "cherry", 42, False)`, `('element',)` |
| Set            | `set`     | Unordered, non-indexed collection of unchangeable items                         | `{"apple", "banana", "cherry", 42, False}`                 |
| Dictionary     | `dict`    | Collection of key-value pairs, where the key is unique.<br/>Ordered since v3.7. | `{'name': 'John', 'age': 30}`                              |

</details>

_Variables_ store values so that they can be reused later.<br/>
They can be reassigned to hold a different value later in the code. That value can be null.<br/>
_Declaring_ variables requires assigning them a value.<br/>
Python is _dynamically_ typed. A variable can be assigned a value of  **any** type.<br/>
Since v3.5, the syntax allows _hinting_ (but _not_ forcing) what type a variable is holding.

<details style='padding: 0 0 1rem 1rem'>

```py
# Declaring variables

the_null_value = None
hinted_null_value: None = None

a_boolean = True
a_hinted_boolean: bool = False

a_string = 'some string'
a_hinted_string: str = "Hello, world!"

an_integer = 123456
a_more_convenient_way_to_write_big_numbers: int = 1_000_000
a_floating_point_number = 3.1
a_complex_number = 1j

a_list = [ 'apple', 7, True ]
a_list_with_only_1_element = [ 'pineapple' ]
an_empty_list = []
a_tuple = ( "kiwi", 4j, 'cherry', 42, False )
a_tuple_with_only_1_element = ( 'lemon', )     # requires the final ','
an_empty_tuple = ()
a_set = { "banana", "orange", 21, False }

a_dictionary = { "brand": "Ford", 'model':"Mustang", "year": 1964 }
an_empty_dictionary = {}


# Use variables

print("a_boolean:", a_boolean)
a_new_string = a_hinted_string + " " + a_string
a_specific_value_from_a_sequence = a_list[2]
a_specific_value_from_a_mapping = a_dict['brand']


# Getting variables' type

type(the_null_value)            # -> <class 'NoneType'>
type(a_boolean)                 # -> <class 'bool'>
type(a_string)                  # -> <class 'str'>
type(an_integer)                # -> <class 'int'>
type(a_floating_point_number)   # -> <class 'float'>
type(a_complex_number)          # -> <class 'complex'>
type(a_list)                    # -> <class 'list'>
type(a_tuple)                   # -> <class 'tuple'>
type(a_set)                     # -> <class 'set'>
type(a_dictionary)              # -> <class 'dict'>


# Convert between types

bool('some string')                   # -> True
bool(0)                               # -> False
int(2.8)                              # -> 2
int('10')                             # -> 10
float(28)                             # -> 28.0
float('42')                           # -> 42.0
complex(21)                           # -> (21+0j)
str(False)                            # -> 'False'
str(1)                                # -> '1'
list(("apple", "banana", "cherry"))   # -> ['apple', 'banana', 'cherry']
tuple(["apple", "banana", "cherry"])  # -> ('apple', 'banana', 'cherry')
set(['banana', 'cherry', 'apple'])    # -> {'banana', 'cherry', 'apple'}
tuple({"some": "dict"})               # -> ('some',)
set({"some": "dict"})                 # -> {'some'}
```

</details>

Prefer formatting/interpolating strings using _f-strings_.

<details style='padding: 0 0 1rem 1rem'>

```py
f"Hello, {name}. You are {age:03d} years old."
F'{name.lower()} is funny.'
```

</details>

Multiple instructions can be given in line when separated by `;`.

<details style='padding: 0 0 1rem 1rem'>

These are functionally the same:

```py
some_string = 'hello world'
print(some_string)
```

```py
some_string = 'hello world' ; print(some_string)
```

</details>

`except` clauses may name multiple exceptions as a parenthesized tuple

<details style='padding: 0 0 1rem 1rem'>

```py
try: pass
except (IDontLikeYouException, YouAreBeingMeanException) as e: raise
```

</details>

_[Virtual environments]_ allow managing dependencies separately for different projects.<br/>
Prefer giving each project its own, private, virtual environment.

Generic notes:

```py
# Make iterables immutable
an_immutable_iterable = frozenset(some_mutable_iterable)

# Get lengths
print(len(a_list))
print(len(a_dict))

# Unset variables
kwargs = None  # rebinds the variable, and lets the garbage collector take care of memory from here
del kwargs     # deletes the variable's reference immediately

# Ask users for input
print("Enter your name:") ; name = input() ; print(f"Hello {name}")

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
if 'key_name' in dictionary: …

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
print(os.environ['HOME'])
print(os.environ.get('LOG_LEVEL', default=logging.INFO))
print(os.getenv('GITLAB_TOKEN'))
print(os.getenv('AWS_PROFILE', default='default'))

# Define functions
def function_name(): pass
def function_with_arguments(arg1, arg2 = None): pass
def function_with_type_hinting(arg1: str, arg2: bool | None = False) -> str | None: pass  # from 3.10

# Avoid taking actions
# … or writing code for the moment
if 'key_name' in dictionary: pass
def some_function(): pass
class some_class: pass

# Get function name from inside them
def function_using_inspect():
    import inspect
    print(inspect.stack()[0][3])  # -> 'function_using_inspect'
def function_using_sys():
    import sys
    print(sys._getframe().f_code.co_name)  # -> 'function_using_sys'

# Configure logging per function
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

Type hinting for functions (since Python 3.5):

```py
def format_phone_number_old(phone: typing.Optional[str] = None): pass  # python 3.5 to 3.10
def format_phone_number(phone: str|None) -> None: pass                 # since python 3.10
```

Working with time:

```py
from datetime import datetime
today = datetime.today().strftime('%Y%m%d')

# AWS format: '2026-02-12T10:29:37+00:00'
datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
```

## Learning material

- W3CSchools' [Python tutorial][w3cschools python tutorial].
- Python's official [documentation].

Fast-track:

1. Learn what is Object-Oriented Programming.<br/>
   At least in its basic concepts.
1. Read code made by others.<br/>
   Goal: understand that code.
1. Reimplement or improve existing pieces of code.<br/>
   Goal: understand the reasoning behind that code.
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
1. Creates a `lib/pythonX.Y/site-packages` subdirectory (`Lib\site-packages` on Windows).
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
| [tqdm]               | Simplified parallelization using [concurrent.futures] and progress bars  |
| [typer]              | CLI applications                                                         |

## Performances

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


### Parallelizing tasks

TODO

Refer [concurrent.futures] and [tqdm].<br/>
See also [Using tqdm with concurrent.futures in Python].

### Lazy formatting

Defers string formatting until it's actually needed.

Some modules (e.g. `lazy_object_proxy` and `logging`) allow deferring any computation, _including_ string formatting,
until the result is accessed.<br/>
F-strings and the `.format()` function are eager and interpolate the string immediately.

Modules supporting lazy formatting encourage users to pass the string's template and arguments separately.<br/>
The handler, then, only performs the string interpolation if the string is actually printed out.

<details style='padding: 0 0 1rem 1rem'>
  <summary>Example: <code>logging</code></summary>

```diff
- logging.debug(f"Processing item {item_id} with value {value}")
+ logging.debug("Processing item %s with value %s", item_id, value)
```

Unless the log level is set to `DEBUG`, this debug message is never formatted.

</details>

The performance difference is negligible for simple variables like integers or strings.<br/>
If arguments involve expensive operations, e.g. calling `repr()` on large objects, serializing data, or computing
values just for a log message, the lazy approach avoids that cost entirely when the string is not accessed.

Python does evaluate function arguments before the call, but it is the logging module itself that decides whether to
combine the template and values if one is passing them separately.

An alternative is to wrap expensive computations in an object whose `__str__` function is only called when needed.

<details style='padding: 0 0 1rem 1rem'>

```py
class LazyFormat:
    def __init__(self, func):
        self.func = func
    def __str__(self):
        return self.func()

logging.debug("Expensive result: %s", LazyFormat(lambda: costly_computation()))
```

</details>

## Plugin systems

### Self-registration via decorator

Plugins manage themselves.<br/>
Adding a new plugin is just a matter of dropping in a `.py` file using a decorated function.<br/>
No need to manually update lists or registries.

See the [experiment](./experiments/plugin_systems/self-registration_via_decorator/README.md).

## Packaging applications

TODO

## Further readings

- [Using tabulation in Python logging format]
- [Python Virtual Environments: A Primer]
- [mypy documentation]
- [Browser Automation in Python: Playwright, Selenium & More]

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
[Documentation]: https://docs.python.org/
[install packages in a virtual environment using pip and venv]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
[venv — creation of virtual environments]: https://docs.python.org/3/library/venv.html

<!-- Others -->
[bitmath]: https://bitmath.readthedocs.io/en/latest/module.html
[boto3]: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
[Browser Automation in Python: Playwright, Selenium & More]: https://www.glukhov.org/post/2026/02/playwright-vs-selenium-puppeteer-lambdatest-zenrows/
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
[w3cschools python tutorial]: https://www.w3schools.com/python
[when should i use a map instead of a for loop?]: https://stackoverflow.com/questions/1975250/when-should-i-use-a-map-instead-of-a-for-loop
