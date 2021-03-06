# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-06 19:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trac',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('trac_type', models.IntegerField(choices=[(1, 'Like'), (2, 'Star'), (3, 'Watch'), (4, 'Follow'), (5, 'Bookmark')])),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trac', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'trac',
                'verbose_name_plural': 'tracs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='trac',
            unique_together=set([('user', 'content_type', 'object_id', 'trac_type')]),
        ),
    ]
