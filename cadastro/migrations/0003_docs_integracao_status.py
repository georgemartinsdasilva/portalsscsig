# Generated by Django 2.0.5 on 2018-07-22 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0002_auto_20180719_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='docs_integracao',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
