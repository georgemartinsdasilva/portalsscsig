# Generated by Django 2.0.5 on 2018-07-20 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hse', '0004_auto_20180717_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aux_table',
            name='status',
            field=models.CharField(max_length=55),
        ),
    ]
