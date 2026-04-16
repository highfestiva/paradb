import os
import time


def file_replace_retry(src: str, dst: str, retries: int = 5):
    for loop in range(retries):
        try:
            os.replace(src, dst)
            break
        except BaseException as ex:
            if loop >= retries - 1:
                raise ex
            time.sleep(0.001)
