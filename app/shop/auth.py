"""Sign-in lockout (security analysis F4, 2026-11-06).

Failed attempts are counted per email address in Django's cache. After LOGIN_MAX_FAILURES
the account cannot sign in for LOGIN_LOCK_MINUTES, even with the right password. The default
cache lives in the server process, so a restart clears the count; that suits one server for
two stores. A multi-process deployment needs a shared cache (database or Redis) for the count
to hold across processes.
"""
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache

LOCKED_MESSAGE = ("Too many failed sign-ins for this account. Wait {minutes} minutes and try again, "
                  "or ask a Manager or the Owner to check the account.")


def _key(email):
    return "qp-login-fail:" + (email or "").strip().lower()


def failures(email):
    return cache.get(_key(email), 0)


def is_locked(email):
    return failures(email) >= settings.LOGIN_MAX_FAILURES


def record_failure(email):
    key, timeout = _key(email), settings.LOGIN_LOCK_MINUTES * 60
    if not cache.add(key, 1, timeout):
        try:
            count = cache.incr(key)
        except ValueError:  # expired between add and incr
            cache.set(key, 1, timeout)
        else:
            cache.touch(key, timeout)  # the lock runs from the latest failure
            return count
    return 1


def clear_failures(email):
    cache.delete(_key(email))


class LockoutAuthenticationForm(AuthenticationForm):
    locked = False

    def clean(self):
        email = self.cleaned_data.get("username")
        if is_locked(email):
            self.locked = True
            raise forms.ValidationError(LOCKED_MESSAGE.format(minutes=settings.LOGIN_LOCK_MINUTES), code="locked")
        try:
            cleaned = super().clean()
        except forms.ValidationError:
            record_failure(email)
            raise
        clear_failures(email)
        return cleaned
