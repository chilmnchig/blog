# Generated by Django 3.1.3 on 2020-11-21 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='montyhole',
            name='change',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='montyhole',
            name='judge',
            field=models.BooleanField(default=False),
        ),
    ]
