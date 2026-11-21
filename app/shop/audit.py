"""Security events use explicit, non-secret details; never copy request bodies or credentials."""
import hashlib

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import AuditEvent


def record(action, actor=None, target=None, *, store=None, outcome="Success", **details):
    actor = actor if actor is not None and actor.is_authenticated and actor.pk else None
    return AuditEvent.objects.create(
        action=action, actor=actor, store=store or getattr(actor, "store", None), outcome=outcome,
        target_type=target._meta.model_name if target is not None else "",
        target_id=str(target.pk) if target is not None else "", details=details)


def login_identifier(email):
    return hashlib.sha256((email or "").strip().lower().encode()).hexdigest()


@receiver(user_logged_in, dispatch_uid="shop.audit.login")
def signed_in(sender, request, user, **kwargs):
    record("sign_in", user)


@receiver(user_logged_out, dispatch_uid="shop.audit.logout")
def signed_out(sender, request, user, **kwargs):
    record("sign_out", user)


@receiver(user_login_failed, dispatch_uid="shop.audit.login_failed")
def sign_in_failed(sender, credentials, request, **kwargs):
    # A hash correlates attempts without retaining the supplied login or password.
    record("sign_in", outcome="Failure", login_hash=login_identifier(credentials.get("username")))


def viewed_passcode(user, job):
    from .crypto import decrypt_passcode
    from .permissions import can_see_passcode
    if not job.device_passcode or not can_see_passcode(user, job):
        return None
    value = decrypt_passcode(job.device_passcode)
    if value:
        record("passcode_view", user, job, store=job.store)
    return value
