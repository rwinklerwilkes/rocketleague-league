# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_first_name', models.CharField(max_length=200)),
                ('player_last_name', models.CharField(max_length=200)),
                ('player_nickname', models.CharField(max_length=200)),
                ('lifetime_goals', models.IntegerField(default=0)),
                ('lifetime_assists', models.IntegerField(default=0)),
                ('lifetime_saves', models.IntegerField(default=0)),
                ('lifetime_shots', models.IntegerField(default=0)),
                ('lifetime_points', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-player_last_name'],
            },
        ),
    ]
