#!/usr/bin/env python3

# https://docs.gitlab.com/api/users/
# https://python-gitlab.readthedocs.io/en/stable/api-usage.html

import csv
import gitlab
import json
import os
import logging
import sys
from prettytable import PrettyTable

logging.basicConfig(level=logging.INFO)

GITLAB_BASE_URL = os.environ.get('GITLAB_BASE_URL')
if not GITLAB_BASE_URL:
    logging.error('GITLAB_BASE_URL must be set')
    sys.exit(1)

GITLAB_TOKEN = os.environ.get('GITLAB_TOKEN')
if not GITLAB_TOKEN:
    logging.error('GITLAB_TOKEN must be set')
    sys.exit(1)

PRINT_USERS_TABLE = bool(os.environ.get('PRINT_USERS_TABLE', True))
SAVE_USERS_CSV = bool(os.environ.get('SAVE_USERS_CSV', False))
GET_USER_MEMBERSHIPS = bool(os.environ.get('GET_USER_MEMBERSHIPS', False))

USERS_HEADERS = ['Name', 'Username', 'ID', 'Email', '2FA', 'State']
if GET_USER_MEMBERSHIPS: USERS_HEADERS.append('Memberships')

if __name__ == '__main__':
    gl = gitlab.Gitlab(url=GITLAB_BASE_URL, private_token=GITLAB_TOKEN, per_page=100)

    # logging.info('Listing human users...')
    # if PRINT_USERS_TABLE:
    #     table = PrettyTable()
    #     table.field_names = USERS_HEADERS
    # if SAVE_USERS_CSV:
    #     with open('human_users.csv', mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(USERS_HEADERS)
    # for human_user in gl.users.list(get_all=True, iterator=True, query_parameters={'humans': True, 'order_by': 'name', 'sort': 'asc'}):
    #     row = [human_user.name, human_user.username, human_user.id, human_user.email, human_user.two_factor_enabled, human_user.state]
    #     if GET_USER_MEMBERSHIPS: row.append(human_user.memberships)
    #     if PRINT_USERS_TABLE:
    #         table.add_row(row)
    #     if SAVE_USERS_CSV:
    #         with open('human_users.csv', mode='a', newline='') as file:
    #             writer = csv.writer(file)
    #             writer.writerow(row)
    # if PRINT_USERS_TABLE:
    #     print(table)

    logging.info('Listing non-human users...')
    if PRINT_USERS_TABLE:
        table = PrettyTable()
        table.field_names = USERS_HEADERS
    if SAVE_USERS_CSV:
        with open('non_human_users.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(USERS_HEADERS)
    for non_human_user in gl.users.list(get_all=True, iterator=True, query_parameters={'exclude_humans': True, 'order_by': 'name', 'sort': 'asc'}):
        row = [non_human_user.name, non_human_user.username, non_human_user.id, non_human_user.email, non_human_user.two_factor_enabled, non_human_user.state]
        if GET_USER_MEMBERSHIPS: row.append(non_human_user.memberships.list(get_all=True, as_list=True))  # FIXME
        if PRINT_USERS_TABLE:
            table.add_row(row)
        if SAVE_USERS_CSV:
            with open('non_human_users.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)
    if PRINT_USERS_TABLE:
        print(table)