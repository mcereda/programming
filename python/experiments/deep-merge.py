#!python3

import logging
from collections.abc import MutableMapping, MutableSequence

logging.basicConfig(level=logging.DEBUG)

d1 = {
    'listen_address': '0.0.0.0:9090',
    'runners': [
        {
            'name': "ruby-2.7-docker",
            'url': "https://CI/",
            'token': "TOKEN",
            'limit': 0,
            'executor': "docker",
            'builds_dir': "",
            'shell': "",
            'environment': ["ENV=value", "LC_ALL=en_US.UTF-8"],
            'clone_url': "http://gitlab.example.local",
        },
        {
            'name': "ruby",
            'url': "https://CI/",
            'token': "TOKEN",
        }
    ]
}
d2 = {
    'concurrent': 24,
    'listen_address': '0.0.0.0:9292',
    'runners': [{
        'name': "ruby-2.7-docker",
        'url': "https://CI/",
        'token': "NEKOT",
        'limit': 25,
        'executor': "docker+machine",
        'builds_dir': "",
        'shell': "/bin/fish",
        'environment': ["ENV=value", "LC_ALL=en_US.UTF-8"],
        'clone_url': "http://gitlab.example.local",
    }]
}

logging.info(f'd1: {d1}')
logging.info(f'd2: {d2}')

def merge_dicts(
    *args: MutableMapping,
    recursive: bool=True,
    list_merge_key: str=None,
    list_merge_strategy: str='replace'
) -> dict:
    """
    FIXME
    """

    # remove all empty dicts from the arguments so they are not processed later
    nonempty_args = tuple(a for a in args if a != {})
    logging.debug(f'nonempty_args: {nonempty_args}')

    if nonempty_args == []:
        result = {}
    else:
        # copy over the first element directly, as it will be the base for
        # merging; iterate on the rest
        result = nonempty_args[0].copy()
        logging.debug(f'result: {result}')
        for arg in nonempty_args[1:]:
            logging.debug(f'arg: {arg}')
            for k, v in arg.items():
                if k not in result.keys():
                    # import the new key-value pair and go straight to the next
                    # from this point on, we know the key is in the result
                    result[k] = v
                    continue
                else:
                    if \
                        isinstance(result[k], MutableMapping) and \
                        isinstance(v, MutableMapping):
                        # both the existing element and the new one with the
                        # same key are dicts: recurse if requested, or just
                        # override the existing value otherwise
                        if recursive:
                            result[k] = merge(result[k], v, recursive)
                        else:
                            result[k] = v
                        continue
                    if \
                        isinstance(result[k], MutableSequence) and \
                        isinstance(v, MutableSequence):
                        # both the existing element and the new one with the
                        # same key are lists: merge depending on the
                        # 'list_merge_strategy' argument
                        if list_merge_strategy == 'replace':
                            # replace the existing value
                            result[k] = v
                        elif list_merge_strategy == 'append':
                            # add the new values to the existing list
                            result[k] = result[k] + v
                        elif list_merge_strategy == 'prepend':
                            # prepend the new values to the existing list
                            result[k] = v + result[k]
                        elif list_merge_strategy == 'append_rp':
                            # append all new elements to all the existing ones
                            # that are not in the new set already
                            # _rp stands for "remove present"
                            result[k] = [z for z in result[k] if z not in v] + v
                        elif list_merge_strategy == 'prepend_rp':
                            # same as 'append_rp' but new elements are prepend
                            result[k] = v + [z for z in result[k] if z not in v]
                        else: pass
                            # 'keep'
                            # keep x value even if y it's of higher priority
                            # it's done by not changing x[key]
                        continue
                    else:
                        # just override the existing value
                        result[k] = v
    return result

logging.info(f'final (replace): {merge_dicts(d1, d2)}')
logging.info(f'final (append): {merge_dicts(d1, d2, list_merge_strategy="append")}')
logging.info(f'final (append_rp): {merge_dicts(d1, d2, list_merge_strategy="append_rp")}')
logging.info(f'final (prepend): {merge_dicts(d1, d2, list_merge_strategy="prepend")}')
logging.info(f'final (prepend_rp): {merge_dicts(d1, d2, list_merge_strategy="prepend_rp")}')
logging.info(f'final (keep): {merge_dicts(d1, d2, list_merge_strategy="keep")}')
