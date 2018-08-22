# Generated by Django 2.1 on 2018-08-21 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zkcluster', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='force_udp',
            field=models.BooleanField(default=False, verbose_name='udp'),
        ),
        migrations.AddField(
            model_name='terminal',
            name='password',
            field=models.IntegerField(default=0, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attendances', to='zkcluster.User'),
        ),
    ]
