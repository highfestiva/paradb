"""Document write locking — per-partition RWLock and per-document-ID lock."""

import time
import threading
from shared.rwlock import RWLock


# Per-partition halt locks (partition_index -> RWLock).
# Normal writes acquire for_reading; orchestrator halt acquires for_writing.
_partition_locks: dict[int, RWLock] = {}
_partition_locks_mutex = threading.Lock()

# Per-document-ID write locks to serialize concurrent writes to the same document.
_document_locks: set[str] = set()
_document_locks_mutex = threading.Lock()


class DocLock:
    def __init__(self, doc_id):
        self.doc_id = doc_id

    def __enter__(self):
        for _ in range(100):
            with _document_locks_mutex:
                if self.doc_id not in _document_locks:
                    _document_locks.add(self.doc_id)
                    break
            print(f'waiting for document {self.doc_id} to be freed')
            time.sleep(0.01)
        else:
            raise TimeoutError("Unable to get document write access")

    def __exit__(self, exc_type, exc, tb):
        with _document_locks_mutex:
            _document_locks.remove(self.doc_id)


def get_partition_lock(partition_index: int) -> RWLock:
    """Get or create the RWLock for a partition."""
    with _partition_locks_mutex:
        if partition_index not in _partition_locks:
            _partition_locks[partition_index] = RWLock()
        return _partition_locks[partition_index]


def get_document_lock(doc_id: str) -> DocLock:
    return DocLock(doc_id)


def reset():
    """Reset all locks (for testing)."""
    with _partition_locks_mutex:
        _partition_locks.clear()
    with _document_locks_mutex:
        _document_locks.clear()
