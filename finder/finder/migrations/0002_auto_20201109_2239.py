# Generated by Django 3.1.2 on 2020-11-09 22:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='username',
            field=models.CharField(default='admin', max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='startdate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='event start date'),
        ),
    ]