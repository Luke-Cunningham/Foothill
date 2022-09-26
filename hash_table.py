import math
import copy
from enum import Enum


class HashEntry:
    class State(Enum):
        ACTIVE = 0
        EMPTY = 1
        DELETED = 2

    def __init__(self, data=None):
        self._data = data
        self._state = HashEntry.State.EMPTY


class HashQP:
    class NotFoundError(Exception):
        pass

    INIT_TABLE_SIZE = 97
    INIT_MAX_LAMBDA = .49

    def __init__(self, table_size=None):

        if table_size is None or table_size < HashQP.INIT_TABLE_SIZE:
            self._table_size = self._next_prime(HashQP.INIT_TABLE_SIZE)
        else:
            self._table_size = self._next_prime(table_size)
        self._buckets = [HashEntry() for _ in range(self._table_size)]
        self._max_lambda = HashQP.INIT_MAX_LAMBDA
        self._size = 0
        self._load_size = 0

    def _internal_hash(self, item):
        return hash(item) % self._table_size

    def _next_prime(self, floor):
        # loop doesn't work for 2 or 3
        if floor <= 2:
            return 2
        elif floor == 3:
            return 3
        if floor % 2 == 0:
            candidate = floor + 1
        else:
            candidate = floor

        while True:
            # we know candidate is odd.  check for divisibility by 3
            if candidate % 3 != 0:
                loop_lim = int((math.sqrt(candidate) + 1) / 6)
                # now we can check for divisibility by 6k +/- 1 up to sqrt
                for k in range(1, loop_lim + 1):
                    if candidate % (6 * k - 1) == 0:
                        break
                    if candidate % (6 * k + 1) == 0:
                        break
                    if k == loop_lim:
                        return candidate
            candidate += 2

    def _find_pos(self, data):
        kth_odd_number = 1
        bucket = self._internal_hash(data)
        while self._buckets[bucket]._state != HashEntry.State.EMPTY and \
                self._buckets[bucket]._data != data:
            bucket += kth_odd_number
            kth_odd_number += 2
            if bucket >= self._table_size:
                bucket -= self._table_size
        return bucket
