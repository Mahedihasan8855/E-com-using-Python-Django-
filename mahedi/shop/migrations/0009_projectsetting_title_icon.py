# Generated by Django 3.1.4 on 2020-12-14 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_projectsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsetting',
            name='title_icon',
            field=models.ImageField(blank=True, null=True, upload_to='icon/'),
        ),
    ]
