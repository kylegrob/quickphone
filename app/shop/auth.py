"""Sign-in lockout (security analysis F4, 2026-11-06).

Failed attempts are counted per email address in Django's cache. After LOGIN_MAX_FAILURES
the account cannot sign in for LOGIN_LOCK_MINUTES, even with the right password. The default
cache lives in the server process, so a restart clears the count; that suits one server for
two stores. A multi-process deployment needs a shared cache (database or Redis) for the count
to hold across processes.

The sign-in page says why a sign-in failed (2026-11-20): a locked account is told it is locked
and for how long, the last tries before a lock are warned, and a turned-off account is told so.
A lock ends only by itself, after LOGIN_LOCK_MINUTES; nobody can end it early.
"""
import math
import time

from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache

LOCKED_MESSAGE = "This account is locked after {failures} failed sign-ins. Try again in {minutes} minute{plural}."
WRONG_MESSAGE = "Email or password is not correct."
WARN_MESSAGE = " {left} more failed {tries} will lock this account for {minutes} minutes."
INACTIVE_MESSAGE = "This account is turned off. Ask a Manager or the Owner to turn it back on."
WARN_WHEN_LEFT = 2  # warn on the last tries before the lock


def _key(email):
    return "qp-login-fail:" + (email or "").strip().lower()


def _until_key(email):
    return "qp-login-until:" + (email or "").strip().lower()


def failures(email):
    return cache.get(_key(email), 0)


def is_locked(email):
    return failures(email) >= settings.LOGIN_MAX_FAILURES


def minutes_left(email):
    """Whole minutes until the lock ends, at least 1 while locked."""
    until = cache.get(_until_key(email))
    if until is None:
        return settings.LOGIN_LOCK_MINUTES
    return max(1, math.ceil((until - time.time()) / 60))


def record_failure(email):
    key, timeout = _key(email), settings.LOGIN_LOCK_MINUTES * 60
    if cache.add(key, 1, timeout):
        count = 1
    else:
        try:
            count = cache.incr(key)
        except ValueError:  # expired between add and incr
            cache.set(key, 1, timeout)
            count = 1
        else:
            cache.touch(key, timeout)  # the lock runs from the latest failure
    if count >= settings.LOGIN_MAX_FAILURES:
        cache.set(_until_key(email), time.time() + timeout, timeout)
    return count


def clear_failures(email):
    cache.delete_many([_key(email), _until_key(email)])


def locked_message(email):
    minutes = minutes_left(email)
    return LOCKED_MESSAGE.format(failures=settings.LOGIN_MAX_FAILURES, minutes=minutes,
                                 plural="" if minutes == 1 else "s")


class LockoutAuthenticationForm(AuthenticationForm):
    locked = False
    error_messages = {**AuthenticationForm.error_messages, "invalid_login": WRONG_MESSAGE,
                      "inactive": INACTIVE_MESSAGE}

    def clean(self):
        email = self.cleaned_data.get("username")
        if is_locked(email):
            from .audit import record, login_identifier
            record("sign_in", outcome="Failure", login_hash=login_identifier(email), locked=True)
            self.locked = True
            raise forms.ValidationError(locked_message(email), code="locked")
        try:
            cleaned = super().clean()
        except forms.ValidationError:
            if self._inactive_with_right_password(email):
                raise forms.ValidationError(INACTIVE_MESSAGE, code="inactive") from None
            count = record_failure(email)
            left = settings.LOGIN_MAX_FAILURES - count
            if left <= 0:
                self.locked = True
                raise forms.ValidationError(locked_message(email), code="locked") from None
            message = WRONG_MESSAGE
            if left <= WARN_WHEN_LEFT:
                message += WARN_MESSAGE.format(left=left, tries="try" if left == 1 else "tries",
                                               minutes=settings.LOGIN_LOCK_MINUTES)
            raise forms.ValidationError(message, code="invalid_login") from None
        clear_failures(email)
        return cleaned

    def _inactive_with_right_password(self, email):
        """Only someone who knows the password learns the account is turned off."""
        from .models import Employee
        user = Employee.objects.filter(email__iexact=(email or "").strip()).first()
        return bool(user and not user.active_flag and user.check_password(self.cleaned_data.get("password") or ""))
