# Generated by Django 2.1.15 on 2021-04-28 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210413_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='baidubridgesettings',
            name='enabled',
            field=models.BooleanField(default=False, help_text='Enable Baidu Bridge'),
        ),
    ]