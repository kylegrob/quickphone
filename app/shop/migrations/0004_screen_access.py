from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_device_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenAccess',
            fields=[
                ('screen_access_id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('Owner', 'Owner'), ('Manager', 'Manager'), ('Technician', 'Technician'), ('Front Desk', 'Front Desk')], max_length=12)),
                ('screen', models.CharField(max_length=20)),
                ('allowed', models.BooleanField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.ForeignKey(blank=True, db_column='updated_by_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='shop.employee')),
            ],
            options={'db_table': 'screen_access'},
        ),
        migrations.AddConstraint(
            model_name='screenaccess',
            constraint=models.UniqueConstraint(fields=('role', 'screen'), name='screen_access_uq'),
        ),
        migrations.AddConstraint(
            model_name='screenaccess',
            constraint=models.CheckConstraint(condition=models.Q(('role__in', ['Owner', 'Manager', 'Technician', 'Front Desk'])), name='screen_access_role_ck'),
        ),
    ]
