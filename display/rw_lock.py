import contextlib
from threading import Lock

class RWLock(object):
    """     Reader-Writer lock recipe taken off the internet:     
    http://code.activestate.com/recipes/577803-reader-writer-lock-with-priority-for-writers/     
    Synchronization object used in a solution of so-called second     
    readers-writers problem. In this problem, many readers can simultaneously     
    access a share, and a writer has an exclusive access to this share.     
    Additionally, the following constraints should be met:     
    1) no reader should be kept waiting if the share is currently opened for         
    reading unless a writer is also waiting for the share,     
    2) no writer should be kept waiting for the share longer than absolutely         necessary.     
    The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7]     
    with a modification -- adding an additional lock (C{self.__readers_queue})     
    -- in accordance with [2].     
    Sources:     
    [1] A.B. Downey: "The little book of semaphores", Version 2.1.5, 2008     
    [2] P.J. Courtois, F. Heymans, D.L. Parnas:         
        "Concurrent Control with 'Readers' and 'Writers'",         
        Communications of the ACM, 1971 (via [3])     
    [3] http://en.wikipedia.org/wiki/Readers-writers_problem     """

    #region LightSwitch
    class _LightSwitch(object):
        """An auxiliary "light switch"-like object. The first thread turns on the         
        "switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""
        def __init__(self):
            self._counter = 0
            self._mutex = Lock()

        def acquire(self, lock):
            with self._mutex:
                self._counter += 1
                if self._counter == 1:
                    lock.acquire()

        def release(self, lock):
            with self._mutex:
                self._counter -= 1
                if self._counter == 0:
                    lock.release()

    #endregion

    def __init__(self):
        self._read_switch = RWLock._LightSwitch()
        self._write_switch = RWLock._LightSwitch()
        self._no_readers = Lock()
        self._no_writers = Lock()
        self._readers_queue = Lock()
        """A lock giving an even higher priority to the writer in certain         
        cases (see [2] for a discussion)"""

    @contextlib.contextmanager
    def read_lock(self):
        try:
            self.reader_acquire()
            yield
        finally:
            self.reader_release()

    @contextlib.contextmanager
    def write_lock(self):
        try:
            self.writer_acquire()
            yield
        finally:
            self.writer_release()

    def reader_acquire(self):
        with self._readers_queue:
            with self._no_readers:
                self._read_switch.acquire(self._no_writers)

    def reader_release(self):
        self._read_switch.release(self._no_writers)

    def writer_acquire(self):
        self._write_switch.acquire(self._no_readers)
        self._no_writers.acquire()

    def writer_release(self):
        self._no_writers.release()
        self._write_switch.release(self._no_readers)