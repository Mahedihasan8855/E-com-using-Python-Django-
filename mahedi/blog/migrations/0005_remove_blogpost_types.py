# Generated by Django 3.1.4 on 2020-12-16 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogpost_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='types',
        ),
    ]