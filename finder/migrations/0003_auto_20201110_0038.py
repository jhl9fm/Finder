# Generated by Django 3.1.2 on 2020-11-10 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0002_auto_20201109_2239'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='covidsafetylevel',
            options={'ordering': ['covidsafetylevel']},
        ),
        migrations.AlterModelOptions(
            name='eventtype',
            options={'ordering': ['eventtype']},
        ),
    ]