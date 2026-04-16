import os
import time


def file_replace_retry(src: str, dst: str, retries: int = 5):
    for loop in range(retries):
        try:
            os.replace(src, dst)
            break
        except PermissionError as ex:
            if loop >= retries - 1:
                raise ex
            time.sleep(0.001)


def osfunc_retry(func, retries: int = 3):
    for loop in range(retries):
        try:
            return func()
        except OSError as ex:
            if loop >= retries - 1:
                raise ex
            time.sleep(0.001)
