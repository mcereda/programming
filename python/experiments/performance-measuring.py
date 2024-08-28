#!python3

from timeit import timeit

do = lambda i: i+1

def _for():
    for i in range(1000):
        do(i)

def _list():
    [ do(i) for i in range(1000) ]

def _map():
    map(do, range(1000))

print(f"plain for loop: {timeit(_for, number=100_000)}")
print(f"list constructor: {timeit(_for, number=100_000)}")
print(f"map: {timeit(_for, number=100_000)}")
