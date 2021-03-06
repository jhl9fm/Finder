# Generated by Django 3.1.2 on 2020-11-02 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CovidSafetyLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('covidsafetylevel', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventtype', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('address', models.CharField(max_length=200)),
                ('startdate', models.DateTimeField(verbose_name='event start date')),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('covidsafetylevel', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='finder.covidsafetylevel')),
                ('eventtype', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='finder.eventtype')),
                ('remote', models.BooleanField(blank=True, default=False)),
                ('size', models.IntegerField()),
                ('outdoor', models.BooleanField(blank=True, help_text='Only required if event not remote')),
                ('masks', models.BooleanField(blank=True, help_text='Only required if event not remote')),
                ('distanced', models.BooleanField(blank=True, help_text='Only required if event not remote')),
            ],
        ),
    ]
