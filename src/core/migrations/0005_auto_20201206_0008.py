# Generated by Django 3.1.4 on 2020-12-05 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='symbol_name',
            field=models.TextField(null=True),
        ),
    ]
