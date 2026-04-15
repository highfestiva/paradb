from contextlib import contextmanager
import threading


class RWLock:
    def __init__(self):
        self._lock = threading.Lock()
        self._read_ready = threading.Condition(self._lock)
        self._readers = 0
        self._writer = False
        self._writers_waiting = 0

    def acquire_read(self):
        with self._lock:
            while self._writer or self._writers_waiting > 0:
                self._read_ready.wait()
            self._readers += 1

    def release_read(self):
        with self._lock:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    @contextmanager
    def for_reading(self):
        try:
            self.acquire_read()
            yield
        finally:
            self.release_read()

    def acquire_write(self):
        with self._lock:
            self._writers_waiting += 1
            while self._writer or self._readers > 0:
                self._read_ready.wait()
            self._writers_waiting -= 1
            self._writer = True

    def release_write(self):
        with self._lock:
            self._writer = False
            self._read_ready.notify_all()

    @contextmanager
    def for_writing(self):
        try:
            self.acquire_write()
            yield
        finally:
            self.release_write()
