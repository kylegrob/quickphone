"""Creates the shared cache table used for the sign-in lockout count on a live server.

With debug off, settings.py points Django's cache at the database table qp_cache, so every
Gunicorn worker sees the same count of failed sign-ins. createcachetable does nothing when the
cache is not a database cache (training and tests), and nothing when the table already exists.
"""
from django.core.management import call_command
from django.db import migrations


def create_cache_table(apps, schema_editor):
    call_command("createcachetable", database=schema_editor.connection.alias, verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_screen_access"),
    ]

    operations = [
        migrations.RunPython(create_cache_table, migrations.RunPython.noop),
    ]
