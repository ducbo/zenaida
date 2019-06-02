from django.core.cache import cache

from bruteforceprotection.exceptions import ExceededMaxAttemptsException


class BruteForceProtection(object):

    def __init__(self, cache_key_prefix, key, max_attempts, timeout):
        self.cache_key = f"{cache_key_prefix}_{key}"
        self.max_attempts = max_attempts
        self.timeout = timeout
        self._local_value = None

    def read_total_attempts(self):
        self._local_value = cache.get(self.cache_key)
        return self._local_value if self._local_value else 0

    def increase_total_attempts(self):
        self._local_value = cache.get(self.cache_key)

        if not self._local_value:
            self._local_value = 0
        self._local_value += 1
        cache.set(self.cache_key, self._local_value, timeout=self.timeout)
        return self._local_value

    def register_attempt(self):
        total_attempts = self.read_total_attempts()
        if total_attempts >= self.max_attempts:
            raise ExceededMaxAttemptsException

        self.increase_total_attempts()