# Generated by Django 2.2.5 on 2019-10-03 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsadmain', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admain',
            name='headimg',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='admain',
            name='resume',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
