# -*- coding: utf-8 -*-
"""Retry wrapper for Vertex AI calls with exponential backoff."""
import time
import functools


def with_retry(max_retries=3, base_delay=10):
    """Decorator that retries on 429 RESOURCE_EXHAUSTED errors."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        delay = base_delay * (2 ** (attempt - 1))
                        print(f'  [retry] Attempt {attempt+1}/{max_retries+1}, waiting {delay}s...', flush=True)
                        time.sleep(delay)
                    return fn(*args, **kwargs)
                except Exception as e:
                    if '429' in str(e) or 'RESOURCE_EXHAUSTED' in str(e):
                        if attempt == max_retries:
                            raise
                        continue
                    raise
        return wrapper
    return decorator
