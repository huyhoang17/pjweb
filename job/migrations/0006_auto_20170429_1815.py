# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-29 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_auto_20170429_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobsinfo',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companys.CompanyProfile'),
        ),
    ]