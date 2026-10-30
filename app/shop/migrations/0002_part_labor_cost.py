from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='labor_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddConstraint(
            model_name='part',
            constraint=models.CheckConstraint(condition=models.Q(('labor_cost__gte', 0)), name='part_labor_ck'),
        ),
    ]
