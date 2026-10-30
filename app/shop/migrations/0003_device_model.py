from django.db import migrations, models


def load_starter_list(apps, schema_editor):
    from shop.device_catalog import STARTER_DEVICES
    DeviceModel = apps.get_model("shop", "DeviceModel")
    for device_type, brand, model in STARTER_DEVICES:
        DeviceModel.objects.get_or_create(brand=brand, model=model, defaults={"device_type": device_type})


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_part_labor_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('device_model_id', models.AutoField(primary_key=True, serialize=False)),
                ('device_type', models.CharField(choices=[('Phone', 'Phone'), ('Tablet', 'Tablet'), ('Laptop', 'Laptop'), ('Game console', 'Game console'), ('Other', 'Other')], max_length=20)),
                ('brand', models.CharField(max_length=40)),
                ('model', models.CharField(max_length=60)),
            ],
            options={
                'db_table': 'device_model',
                'ordering': ['brand', 'model'],
                'constraints': [models.UniqueConstraint(fields=('brand', 'model'), name='device_model_uq')],
            },
        ),
        migrations.RunPython(load_starter_list, migrations.RunPython.noop),
    ]
