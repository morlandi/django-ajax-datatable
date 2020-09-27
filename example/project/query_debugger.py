# Adapted from:
# "Django select_related and prefetch_related: Checking how many queries reduce using these methods with an example"
# by Goutom Roy
# https://medium.com/better-programming/django-select-related-and-prefetch-related-f23043fd635d

from django.db import connection, reset_queries
import time
import functools
from ajax_datatable.utils import trace

def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        trace('{func}(): {num_queries} queries ({elapsed:.2f}s)'.format(
            func=func.__qualname__,
            num_queries=end_queries - start_queries,
            elapsed=end - start,
        ))

        # print(f"Function : {func.__name__}")
        # print(f"Number of Queries : {end_queries - start_queries}")
        # print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func
