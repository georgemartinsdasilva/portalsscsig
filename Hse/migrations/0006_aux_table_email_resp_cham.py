# Generated by Django 2.0.5 on 2018-07-20 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hse', '0005_auto_20180720_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='aux_table',
            name='email_resp_cham',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]