# Python

1. [TL;DR](#tldr)
1. [Modules of interest](#modules-of-interest)
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

# Get values from environment variables
import os
print(os.environ('HOME'))
print(os.environ.get('GITLAB_TOKEN', default=None))

# Get function name from inside it
def function_using_inspect():
    import inspect
    print(inspect.stack()[0][3])  # function_using_inspect
def function_using_sys():
    import sys
    print(sys._getframe().f_code.co_name)  # function_using_sys


# Set logging per function
def funct(log_level='WARN'):
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

| Module     | Use for                                                                  |
| ---------- | ------------------------------------------------------------------------ |
| [boto3]    | Interact with AWS services                                               |
| [ciso8601] | Convert ISO8601 or RFC3339 datetime strings into Python datetime objects |
| [logging]  | Kinda self-explanatory, isn't it?                                        |
| [psycopg]  | Interact with PostgreSQL databases                                       |

## Further readings

- [Using tabulation in Python logging format]

### Sources

- [venv — creation of virtual environments]
- [Install packages in a virtual environment using pip and venv]
- [Python module import: single-line vs multi-line]
- [Python tutorial]
- [Convert List to Set]
- [When should I use a Map instead of a For Loop?]

<!--
  Reference
  ═╬═Time══
  -->

<!-- Upstream -->
[install packages in a virtual environment using pip and venv]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
[venv — creation of virtual environments]: https://docs.python.org/3/library/venv.html

<!-- Others -->
[boto3]: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
[ciso8601]: https://pypi.org/project/ciso8601/
[convert list to set]: https://pythonexamples.org/python-convert-list-to-set/
[logging]: https://docs.python.org/3/library/logging.html
[psycopg]: https://www.psycopg.org/
[python module import: single-line vs multi-line]: https://stackoverflow.com/questions/15011367/python-module-import-single-line-vs-multi-line
[python tutorial]: https://www.w3schools.com/python
[using tabulation in python logging format]: https://stackoverflow.com/questions/2777169/using-tabulation-in-python-logging-format#26145642
[when should i use a map instead of a for loop?]: https://stackoverflow.com/questions/1975250/when-should-i-use-a-map-instead-of-a-for-loop
