# Python

1. [TL;DR](#tldr)
1. [Modules of interest](#modules-of-interest)
1. [Parallelization](#parallelization)
1. [Further readings](#further-readings)
   1. [Sources](#sources)

## TL;DR

```sh
python3.12 -m 'venv' '.venv'

source '.venv/bin/activate'
source '.venv/bin/activate.fish'

python3 -m pip install -r 'requirements.txt'

python3 -m pip freeze

deactivate
```

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

## Further readings

- [Using tabulation in Python logging format]

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
[tqdm]: https://tqdm.github.io/
[using tabulation in python logging format]: https://stackoverflow.com/questions/2777169/using-tabulation-in-python-logging-format#26145642
[using tqdm with concurrent.futures in python]: https://rednafi.com/python/tqdm_progressbar_with_concurrent_futures/
[when should i use a map instead of a for loop?]: https://stackoverflow.com/questions/1975250/when-should-i-use-a-map-instead-of-a-for-loop
