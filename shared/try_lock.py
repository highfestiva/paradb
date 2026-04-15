import threading


class TryLock:
    def __init__(self):
        self.mutex = threading.Lock()
        self.is_locked = False

    def __enter__(self):
        self.is_locked = self.mutex.acquire(blocking=False)
        return self.is_locked

    def __exit__(self, exc_type, exc, tb):
        if self.is_locked:
            self.mutex.release()
            self.is_locked = False
