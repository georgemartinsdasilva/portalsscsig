# Generated by Django 2.0.5 on 2018-07-22 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0003_docs_integracao_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='docs_integracao',
            name='email_emp',
            field=models.CharField(default='none', max_length=100),
        ),
    ]