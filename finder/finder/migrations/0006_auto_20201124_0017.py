# Generated by Django 3.1.1 on 2020-11-24 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0005_auto_20201118_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='distanced',
            field=models.BooleanField(default=False, help_text='Input only required if event not remote'),
        ),
        migrations.AlterField(
            model_name='event',
            name='masks',
            field=models.BooleanField(default=False, help_text='Input only required if event not remote'),
        ),
        migrations.AlterField(
            model_name='event',
            name='outdoor',
            field=models.BooleanField(default=False, help_text='Input only required if event not remote'),
        ),
    ]
