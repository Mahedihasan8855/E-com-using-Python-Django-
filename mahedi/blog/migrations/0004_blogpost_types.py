# Generated by Django 3.1.4 on 2020-12-16 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201216_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='types',
            field=models.CharField(default='', editable=False, max_length=200),
        ),
    ]
