# Generated by Django 3.1.4 on 2020-12-15 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_projectsetting_title_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsetting',
            name='team1',
            field=models.ImageField(blank=True, null=True, upload_to='icon/'),
        ),
        migrations.AddField(
            model_name='projectsetting',
            name='team2',
            field=models.ImageField(blank=True, null=True, upload_to='icon/'),
        ),
        migrations.AddField(
            model_name='projectsetting',
            name='team3',
            field=models.ImageField(blank=True, null=True, upload_to='icon/'),
        ),
        migrations.AddField(
            model_name='projectsetting',
            name='team4',
            field=models.ImageField(blank=True, null=True, upload_to='icon/'),
        ),
        migrations.AddField(
            model_name='projectsetting',
            name='team5',
            field=models.ImageField(blank=True, null=True, upload_to='icon/'),
        ),
    ]
